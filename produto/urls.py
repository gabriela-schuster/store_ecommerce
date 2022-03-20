from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categoria/<str:cat>/', views.category, name='category'),
    path('produto/<str:slug>/', views.produto, name='produto'),
    path('carrinho/', views.cart, name='cart'),
    path('adicionaraocarrinho/', views.add_to_cart, name='addtocart'),
    path('removerdocarrinho/<str:varid>', views.remove_from_cart, name='removefromcart'),
    path('resumodacompra/', views.summary, name='summary'),
]
