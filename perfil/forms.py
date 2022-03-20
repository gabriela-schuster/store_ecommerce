from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Perfil
from django import forms

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Usuário"
		self.fields['first_name'].label = "Nome"
		self.fields['last_name'].label = "Sobrenome"
		self.fields['last_name'].label = "Sobrenome"
		self.fields['email'].label = "Email"
		self.fields['password1'].label = "Senha"
		self.fields['password2'].label = "Repita a senha"

		for name, field in self.fields.items():
			field.widget.attrs.update(
				{'class': 'input', 'spellcheck': 'false'})


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']

	def __init__(self, *args, **kwargs):
		super(UserEditForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Usuário"
		self.fields['first_name'].label = "Nome"
		self.fields['last_name'].label = "Sobrenome"
		self.fields['last_name'].label = "Sobrenome"
		self.fields['email'].label = "Email"

		for name, field in self.fields.items():
			field.widget.attrs.update(
				{'class': 'input', 'spellcheck': 'false'})


class ProfileForm(ModelForm):
	class Meta:
		model = Perfil
		fields = '__all__'
		exclude = ('user',)

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['cpf'].label = "Cpf (somente números)"

		for name, field in self.fields.items():
			field.widget.attrs.update({'class': 'input'})
