from sys import stdout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ItemPedido, Pedido


def save(req):
	cart = req.session.get('cart')

	if not req.user.is_authenticated:
		messages.error(req, 'é preciso ter uma conta para entrar nesta página')
		return redirect('create-user')
	elif not cart:
		messages.error(req, 'carrinho vazio')
		return redirect('home')

	qtd_total_cart = cart_total_qtd(cart)
	total_cart = cart_total_cost(cart)

	pedido = Pedido(
		user = req.user,
		total = total_cart,
		qtd_total = qtd_total_cart,
		status = 'C'
	)
	pedido.save()

	ItemPedido.objects.bulk_create(
		[
			ItemPedido(
				pedido=pedido,
				produto_nome=v['produto_nome'],
				produto_id=v['produto_id'],
				variacao=v['variacao_nome'],
				variacao_id=v['variacao_id'],
				preco=v['preco_unitario'],
				quantidade=v['quantidade'],
				imagem=v['imagem'],
			) for v in cart.values()
		]
	)

	del req.session['cart']

	context = {
		'qtd_total_cart': qtd_total_cart,
		'total_cart': total_cart,
	}
	# return render(req, 'pay.html', context)
	return redirect('pay')


def pay(req):
	return render(req, 'pay.html')


def listar(req):
	return render(req, 'list.html')


# --------------------------------- helpers ------------------------------------
def cart_total_qtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])


def cart_total_cost(cart):
	return sum(
		[
			item.get('preco_total')
			for item 
			in cart.values()
		]
	)
