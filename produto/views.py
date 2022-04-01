from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Produto, Variacao


def home(req):
	destaques = Produto.objects.filter(destaque=True)

	casacos = Produto.objects.filter(categoria='C')
	preco_minimo_casaco = 100000
	for casaco in casacos:
		if casaco.preco_minimo < preco_minimo_casaco:
			preco_minimo_casaco = casaco.preco_minimo

	moletoms = Produto.objects.filter(categoria='M')
	preco_minimo_moletom = 100000
	for moletom in moletoms:
		if moletom.preco_minimo < preco_minimo_moletom:
			preco_minimo_moletom = moletom.preco_minimo

	blusas = Produto.objects.filter(categoria='B')
	preco_minimo_blusa = 100000
	for blusa in blusas:
		if blusa.preco_minimo < preco_minimo_blusa:
			preco_minimo_blusa = blusa.preco_minimo

	calcas = Produto.objects.filter(categoria='A')
	preco_minimo_calca = 100000
	for calca in calcas:
		if calca.preco_minimo < preco_minimo_calca:
			preco_minimo_calca = calca.preco_minimo
	
	context = {
		'destaques': destaques,
		'preco_minimo_casaco': preco_minimo_casaco,
		'preco_minimo_moletom': preco_minimo_moletom,
		'preco_minimo_blusa': preco_minimo_blusa,
		'preco_minimo_calca': preco_minimo_calca,
	}
	return render(req, 'home.html', context)


def category(req, cat):
	products = Produto.objects.filter(categoria=cat)
	cat_name_full = None

	if cat == "C":
		cat_name_full = 'Casacos'
	elif cat == "M":
		cat_name_full = 'Moletons'
	elif cat == "B":
		cat_name_full = 'Blusas'
	elif cat == "A":
		cat_name_full = 'Calças'

	context = {
		'products': products,
		'cat_name': cat_name_full
	}
	return render(req, 'category.html', context)


def produto(req, slug):
	product = Produto.objects.get(slug=slug)
	context = {'produto': product}

	return render(req, 'product.html', context)


def add_to_cart(req):
	http_referer = req.META.get('HTTP_REFERER')
	variacao_id = req.GET.get('vid')

	# verifying things
	if not variacao_id:
		messages.error(req, 'Selecione o tipo do produto')
		return HttpResponseRedirect(http_referer)

	variacao = get_object_or_404(Variacao, id=variacao_id)
	variation_estoque = variacao.estoque
	produto = variacao.produto

	if variacao.estoque < 1:
		messages.error(req, 'Infelizmente este item está fora de estoque')
		return redirect(http_referer)

	# inicializa sessao do cart se ja nao estiver inicializada
	if not req.session.get('cart'):
		req.session['cart'] = {}
		req.session.save()
	cart = req.session.get('cart')

	# actually adding to cart

	if variacao_id in cart:
		actual_quantity_in_cart = cart[variacao_id]['quantidade']
		actual_quantity_in_cart += 1

		if variation_estoque < actual_quantity_in_cart:
			messages.error(
				req, 
				f'Estoque insuficiente para {actual_quantity_in_cart} {produto.nome}. Apenas {variation_estoque} produtos serão adicionados'
			)
			actual_quantity_in_cart = variation_estoque

		cart[variacao_id]['quantidade'] = actual_quantity_in_cart
		cart[variacao_id]['preco_total'] = variacao.preco * actual_quantity_in_cart
	else:
		cart[variacao_id] = {
			'produto_id': produto.id, 
			'variacao_id': variacao_id,
			'produto_nome': produto.nome, 
			'variacao_nome': variacao.nome, 
			'preco_unitario': variacao.preco,
			'preco_total': variacao.preco,				# total
			'quantidade': 1,
			'slug': produto.slug,
			'imagem': produto.imagem.name,
		}
	
	req.session.save()
	messages.info(req, f'Produto adicionado ao carrinho, {cart[variacao_id]["quantidade"]} total')

	print(cart)
	return HttpResponseRedirect(http_referer)


def cart(req):
	return render(req, 'cart.html')


def remove_from_cart(req, varid):
	http_referer = req.META.get('HTTP_REFERER')

	if not req.session.get('cart'):
		return redirect(http_referer)

	if not varid:
		return redirect(http_referer)

	if varid not in req.session['cart']:
		return redirect(http_referer)
		print('o alguem tentou mecher nos params pra remover do cart')

	product_in_cart = req.session['cart'][varid]
	messages.info(req, f'produto {product_in_cart["produto_nome"]} removido com sucesso')
	# todo: if quantidade > 1 remover 1

	del req.session['cart'][varid]
	req.session.save()
	return HttpResponseRedirect(http_referer)


def summary(req):
	perfil = req.user.perfil_set.get(user=req.user)
	cart = req.session.get('cart')

	context = {
		'perfil': perfil,
		'user': req.user
	}

	# ------------ checking if the quantity of the product in cart is not > than available
	# and changing it as necesary
	cart_variation_ids = [v for v in cart]
	variations = list(
		Variacao.objects.select_related('produto').filter(id__in=cart)
	)

	for variation in variations:
		v_id = str(variation.id)

		estoque = variation.estoque
		qtd_cart = cart[v_id]['quantidade']

		if estoque < qtd_cart:
			cart[v_id]['quantidade'] = estoque
			cart[v_id]['preco_total'] = estoque * cart[v_id]['preco_unitario']
			req.session.save()

			messages.error(req, 'Estoque insuficiente para alguns produtos do seu carrinho, adicionando a quantidade máxima disponível, por favor revise a compra')

			return redirect('cart')

	return render(req, 'summary.html', context)
