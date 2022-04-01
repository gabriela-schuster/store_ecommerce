from django.urls import path
from . import views

urlpatterns = [
	path('salvar/', views.save, name='save'),
	path('listar/', views.listar, name='listar'),
	path('pagar/', views.pay, name='pay'),
]
