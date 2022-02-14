from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Produto, Variacao


def home(req):
	return render(req, 'home.html')


def category(req, cat):
	products = Produto.objects.filter(categoria=cat)
	cat_name_full = None

	if cat == "C":
		cat_name_full = 'Camisas'
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
	# cart = req.session['cart']
	cart = req.session.get('cart')

	if variacao_id in cart:
		actual_quantity_in_cart = cart[variacao_id]['estoque']
		actual_quantity_in_cart += 1

		if variation_estoque < actual_quantity_in_cart:
			messages.error(
				req, 
				f'Estoque insuficiente para {actual_quantity_in_cart} {produto.nome}. Apenas {variation_estoque} produtos serão adicionados'
			)
			actual_quantity_in_cart = variation_estoque

		cart[variacao_id]['estoque'] = actual_quantity_in_cart
		cart[variacao_id]['preco_total'] = variacao.preco * actual_quantity_in_cart
	else:
		cart[variacao_id] = {
			'produto_id': produto.id, 
			'variacao_id': variacao_id,
			'produto_nome': produto.nome, 
			'variacao_nome': variacao.nome, 
			'preco_unitario': variacao.preco,
			'preco_total': variacao.preco,				# total
			'estoque': 1,
			'slug': produto.slug,
			'image': produto.imagem.name,
		}
	
	req.session.save()
	messages.info(req, f'Produto adicionado ao carrinho, {cart[variacao_id]["estoque"]} total')

	print(cart)
	return HttpResponseRedirect(http_referer)


def cart(req):
	return render(req, 'cart.html')