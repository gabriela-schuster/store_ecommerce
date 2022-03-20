from django.contrib import admin
from .models import Perfil


class PerfilAdmin(admin.ModelAdmin):
	list_display = ['user', 'estado', 'cidade']


admin.site.register(Perfil, PerfilAdmin)
