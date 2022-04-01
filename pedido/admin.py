from django.contrib import admin
from .models import Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
	model = ItemPedido
	extra = 1
	list_display = ['produto_name', 'preco', 'quantidade']


class PedidoAdmin(admin.ModelAdmin):
	inlines = [ItemPedidoInline]


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)
