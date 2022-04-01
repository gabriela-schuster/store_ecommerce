from django.urls import path
from . import views

urlpatterns = [
	path('salvar/', views.save, name='save'),
	path('pagar/<int:pk>', views.pay, name='pay'),
	path('listar/', views.list, name='list'),
	path('detalhesdopedido/', views.order_detail, name='order-detail'),
]
