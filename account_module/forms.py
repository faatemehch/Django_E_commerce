from django import forms
from django.contrib.auth.models import User


class LoginForm( forms.Form ):
    username = forms.CharField( widget=forms.TextInput( attrs={'class': 'form-control'} ) )
    password = forms.CharField( widget=forms.PasswordInput( attrs={'class': 'form-control'} ) )


class EditUserAccountModelForm( forms.ModelForm ):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput( attrs={'class': 'form-control'} ),
            'first_name': forms.TextInput( attrs={'class': 'form-control'} ),
            'last_name': forms.TextInput( attrs={'class': 'form-control'} ),
            'email': forms.EmailInput( attrs={'class': 'form-control'} )
        }
