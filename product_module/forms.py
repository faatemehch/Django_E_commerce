from django import forms
from .models import ProductComment


class CommentForm( forms.ModelForm ):
    class Meta:
        model = ProductComment
        fields = ('fullname', 'email', 'message', 'product')
        widgets = {
            'fullname': forms.TextInput( attrs={'class': 'form-control', 'type': "text"} ),
            'email': forms.TextInput( attrs={'class': 'form-control', 'type': "email"} ),
            'message': forms.Textarea(
                attrs={'class': 'form-control', 'rows': "7", 'id': "comment-text-input", 'cols': "80"} ),
            'product': forms.TextInput( attrs={'type': 'hidden'} )

        }
