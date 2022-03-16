from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,DetailView
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
from .models import Sell
from .forms import CreateUserForm

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('accounts:home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('accounts:login')
			

		context = {'form':form}
		return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('accounts:home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('accounts:home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('accounts:login')


@login_required(login_url='accounts:login')
def home(request):
	context = {}
	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='accounts:login')
def buy(request):
	context = {}
	return render(request, 'accounts/buy.html', context)

@login_required(login_url='accounts:login')
def rent(request):
	context = {}
	return render(request, 'accounts/rent.html', context)

class Sell_Create(CreateView):
	model = Sell
	fields = "__all__"
	success_url = reverse_lazy('accounts:home')

class Sell_List(ListView):
	model = Sell
	context_object_name = 'item_list'

class Sell_Details(DetailView):
	model = Sell
	

