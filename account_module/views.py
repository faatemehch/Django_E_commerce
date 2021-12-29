from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


#  login user
def login_view(request):
    if request.user.is_authenticated:
        return redirect( 'product_module:product-list' )
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
