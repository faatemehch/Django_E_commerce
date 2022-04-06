from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from utils.email_services import EmailService
from account_module.models import User
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, FormView
from .forms import (
    LoginForm,
    EditUserAccountModelForm,
    RegisterForm,
    ResetPasswordForm,
    ForgotPasswordForm,
    ActivationCodeForm
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
import random


def generate_integer_active_code(length=6):
    numeral_active_code = ''
    for _ in range(length):
        numeral_active_code += str(random.randint(1, 9))
    return numeral_active_code


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
                register_form.add_error('email', 'email is not valid!')
            else:
                string_active_code = get_random_string(72)
                numeral_active_code = generate_integer_active_code()
                new_user = User(email=email, password=password, gender=gender, username=email, is_active=False,
                                active_code=string_active_code, numeral_active_code=numeral_active_code)
                new_user.set_password(password)
                new_user.save()
                EmailService.send_email('account activation', new_user.email, {'user': new_user},
                                        'emails/active_account.html')

                return render(request, 'emails/check_email.html', {'user': new_user})
                # return redirect(reverse('account_module:login'))
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
    current_user = User.objects.filter(id=request.user.id).first()
    if request.method == 'POST':
        edit_form = EditUserAccountModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
            return redirect('account_module:user-account')
    else:
        edit_form = EditUserAccountModelForm(instance=current_user)
    context = {
        'title': 'user form',
        'edit_form': edit_form,
        'user': current_user
    }
    return render(request, 'account_module/user_edit_form.html', context)


def activation_account_view(request, active_code):
    user = User.objects.filter(active_code__iexact=active_code).first()
    active_form = ActivationCodeForm(request.POST or None)
    if user is not None:
        if not user.is_active:
            if request.method == 'POST':
                if active_form.is_valid():
                    user_active_code = active_form.cleaned_data.get('active_code')
                    if user.numeral_active_code == user_active_code:
                        user.is_active = True
                        user.active_code = get_random_string(72)
                        user.numeral_active_code = generate_integer_active_code()
                        user.save()
                        return redirect(reverse('account_module:login'))
                    else:
                        active_form.add_error('active_code', 'activation code is wrong')
            else:
                context = {
                    'form': active_form,
                    'title': 'account activation'
                }
                return render(request, 'account_module/active_account_page.html', context)
    raise Http404


class ForgotPasswordView(View):
    def get(self, request):
        forgot_pass_form = ForgotPasswordForm()
        context = {'form': forgot_pass_form, 'title': 'forgot password'}
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request):
        forgot_pass_form = ForgotPasswordForm(request.POST)
        if forgot_pass_form.is_valid():
            user_email = forgot_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email=user_email).first()
            if user is not None:
                EmailService.send_email(subject='forgot password', to=user.email, context={'user': user},
                                        template_name='emails/forgot_password_email.html')
            return redirect(reverse('account_module:login'))
        context = {'form': forgot_pass_form, 'title': 'forgot password'}
        return render(request, 'account_module/forgot_password.html', context)


def reset_password_view(request, active_code):
    user = User.objects.filter(active_code__iexact=active_code).first()
    if user is not None:
        reset_pass_form = ResetPasswordForm(request.POST or None)
        if reset_pass_form.is_valid():
            user_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_pass)
            user.active_code = get_random_string(72)
            user.save()
            return redirect(reverse('account_module:login'))
        context = {'form': reset_pass_form, 'title': 'retrieve password'}
        return render(request, 'account_module/reset_password.html', context)
