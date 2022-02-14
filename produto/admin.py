from django.contrib import admin
from .models import Produto, Variacao


class VariationInline(admin.TabularInline):
	model = Variacao
	extra = 1


class ProdutoAdmin(admin.ModelAdmin):
	list_display = ['nome', 'preco_minimo', 'preco_maximo', 'categoria']
	inlines = [VariationInline]


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)

