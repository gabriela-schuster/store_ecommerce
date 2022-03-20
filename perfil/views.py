from multiprocessing import context
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, UserEditForm ,ProfileForm


def create_user(req):
	""" if req.user.is_authenticated:
		return redirect('home') """

	user_form = UserForm()

	if req.method == 'POST':
		user_form = UserForm(req.POST)
		if user_form.is_valid():
			user = user_form.save(commit=False)
			user.save()
			login(req, user)
			return redirect('create-profile')
		else:
			messages.error(req, 'Revise os campos e tente novamente')

	context = {'user_form': user_form}
	return render(req, 'create-user.html', context)


def create_profile(req):
	""" if req.user.is_authenticated:
		return redirect('home') """

	profile_form = ProfileForm()
	
	if req.method == 'POST':
		profile_form = ProfileForm(req.POST)
		if profile_form.is_valid():
			profile = profile_form.save(commit=False)
			user = req.user
			profile.user = user

			profile.save()

			messages.info(req, 'Usuário craido com sucesso, você já pode comprar em nossa loja')
			return redirect('home')
		else:
			messages.error(req, 'Revise os campos e tente novamente')

	context = {'profile_form': profile_form}
	return render(req, 'create-profile.html', context)


def login_user(req):
	""" if req.user.is_authenticated:
		return redirect('home') """

	if req.method == 'POST':
		username = req.POST['username']
		password = req.POST['password']

		user = authenticate(req, username=username, password=password)
		if user != None:
			login(req, user)
			return redirect('home')
		else:
			messages.error(req, 'Username OR password is incorrect')

	return render(req, 'login_user.html')


def logout_user(req):
	logout(req)
	return redirect('home')


def edit_user(req):
	profile = req.user.perfil_set.get()
	profile_form = ProfileForm(instance=profile)
	
	if req.method == 'POST':
		form = ProfileForm(req.POST, instance=profile)
		if form.is_valid():
			form.save()
			messages.info(req, 'Perfil atualizado com sucesso')
			# so browser doesn't save previous form in cache
			return redirect('edit-user')
		else:
			messages.info(req, 'Ocorreu um erro, verifique se há erros e tente novamente')

	context = {'profile_form': profile_form}
	return render(req, 'edit.html', context)


def edit_user_personal(req):
	user = req.user
	user_edit_form = UserEditForm(instance=user)

	if req.method == 'POST':
		form = UserEditForm(req.POST, instance=user)
		if form.is_valid():
			form.save()
			messages.info(req, 'Usuáriuo atualizado com sucesso')
			return redirect('edit-user-personal')
		else:
			messages.info(req, 'Ocorreu um erro, verifique se há erros e tente novamente')

	context = {
		'user_form': user_edit_form,
	}

	return render(req, 'edit-personal.html', context)