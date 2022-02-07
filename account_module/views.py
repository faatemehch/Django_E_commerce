from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from account_module.models import User
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from .forms import LoginForm, EditUserAccountModelForm, RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate


#  login user
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home_module:home-view')
    login_form = LoginForm(request.POST or None)
    context = {
        'title': 'login',
        'login_form': login_form
    }
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        login_form.add_error('username', 'enter you information correctly!')
    return render(request, 'account_module/login_page.html', context)


@login_required(login_url='account_module:login')
def logout_user(request):
    logout(request)
    return redirect('account_module:login')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home_module:home-view')
        register_form = RegisterForm()
        context = {
            'register_form': register_form,
            'title': 'register view'
        }
        return render(request, 'account_module/register_page.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home_module:home-view')
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data.get('email')
            password = register_form.cleaned_data.get('password')
            gender = register_form.cleaned_data.get('gender')
            user_exist = User.objects.filter(email=email).exists()
            if user_exist:
                register_form.add_error(email, 'email is not valid!')
            else:
                new_user = User(email=email, password=password, gender=gender)
                new_user.set_password(password)
                new_user.save()
                return redirect(reverse('account_module:login'))
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register_page.html', context)


class UserAccountView(View, LoginRequiredMixin):
    def get(self, request):
        context = {
            'title': 'user Account'
        }
        return render(request, 'account_module/user_account.html', context)


@login_required(login_url='account_module:login')
def edit_user_info(request):
    edit_form = EditUserAccountModelForm(data=request.POST or None, instance=request.user)
    if request.method == 'POST':
        if edit_form.is_valid():
            edit_form.save()
            return redirect('account_module:user-account')
    context = {
        'title': 'user form',
        'edit_form': edit_form
    }
    return render(request, 'account_module/user_edit_form.html', context)
