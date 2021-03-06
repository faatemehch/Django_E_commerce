from django import forms
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditUserAccountModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'})
        }


gender_choices = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    gender = forms.CharField(widget=forms.Select(choices=gender_choices))
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    avatar = forms.ImageField(required=False)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise forms.ValidationError('password and it\'s repetition must be matched!')


class ActivationCodeForm(forms.Form):
    active_code = forms.CharField(label='active code', widget=forms.TextInput(attrs={'class': 'form-control'}))


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       label='current password')
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='new password')
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='confirm new password')

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password == confirm_new_password:
            return confirm_new_password
        raise forms.ValidationError('new password and it\'s confirmation are not equal')
