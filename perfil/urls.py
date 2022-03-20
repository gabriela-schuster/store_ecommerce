from django.urls import path
from . import views

urlpatterns = [
	path('criar/', views.create_user, name='create-user'),
	path('criarperfil/', views.create_profile, name='create-profile'),
	path('login/', views.login_user, name='login-user'),
	path('editar/', views.edit_user, name='edit-user'),
	path('editarusuario/', views.edit_user_personal, name='edit-user-personal'),
	path('logout/', views.logout_user, name='logout-user'),
]
