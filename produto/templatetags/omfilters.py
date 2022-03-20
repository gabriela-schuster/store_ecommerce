from django.template import Library

register = Library()

@register.filter
def format_price(val):
	return f'{val:.2f}'.replace('.', ',')


@register.filter
def cart_total_cost(cart):
	return sum(
		[
			item.get('preco_total')
			for item 
			in cart.values()
		]
	)

