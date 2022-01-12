from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.views import View


#  login user
def login_view(request):
    if request.user.is_authenticated:
        return redirect( 'home_module:home-view' )
    login_form = LoginForm( request.POST or None )
    context = {
        'title': 'login',
        'login_form': login_form
    }
    if login_form.is_valid():
        username = login_form.cleaned_data.get( 'username' )
        password = login_form.cleaned_data.get( 'password' )
        user = authenticate( username=username, password=password )
        if user is not None:
            login( request, user )
        login_form.add_error( 'username', 'enter you information correctly!' )
    return render( request, 'account_module/login_page.html', context )


@login_required( login_url='account_module:login' )
def logout_user(request):
    logout( request )
    return redirect( 'account_module:login' )


def register_view(request):
    if request.user.is_authenticated:
        return redirect( 'home_module:home-view' )
    register_form = UserCreationForm( request.POST )
    context = {
        'title': 'register',
        'register_form': register_form
    }
    if register_form.is_valid():
        register_form.save()
        return redirect( 'account_module:login' )
    return render( request, 'account_module/register_page.html', context )


class UserAccountView( View ):
    def get(self, request):
        context = {
            'title': 'user Account'
        }
        return render( request, 'account_module/user_account.html', context )
