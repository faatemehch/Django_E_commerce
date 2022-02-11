from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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
    if request.method == 'POST':
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            user = User.objects.filter(username=email).first()
            if user is not None:
                if user.is_active:
                    is_correct = user.check_password(password)
                    if is_correct:
                        login(request, user)
                        return redirect(reverse('account_module:user-account'))
                    else:
                        login_form.add_error('email', 'email or password is incorrect')
                login_form.add_error('email', 'your account must be active first!')
            login_form.add_error('email', 'email or password is incorrect')
    context = {'title': 'login', 'login_form': login_form}
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
                new_user = User(email=email, password=password, gender=gender, username=email)
                new_user.set_password(password)
                new_user.save()
                return redirect(reverse('account_module:login'))
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register_page.html', context)


class UserAccountView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'title': 'user Account'
        }
        return render(request, 'account_module/user_account.html', context)


@login_required(login_url='account_module:login')
def edit_user_info(request):
    if request.method == 'POST':
        edit_form = EditUserAccountModelForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('account_module:user-account')
    else:
        edit_form = EditUserAccountModelForm(instance=request.user)
    context = {
        'title': 'user form',
        'edit_form': edit_form,
        'user': User.objects.filter(username=request.user.username).first()
    }
    return render(request, 'account_module/user_edit_form.html', context)
