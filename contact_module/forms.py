from django import forms
from .models import ContactUs


class ContactUsForm( forms.ModelForm ):
    class Meta:
        model = ContactUs
        fields = ('fullname', 'email', 'subject', 'message_text')
        widgets = {
            'fullname': forms.TextInput( attrs={'class': 'form-control', 'type': "text"} ),
            'email': forms.TextInput( attrs={'class': 'form-control', 'type': "email"} ),
            'subject': forms.TextInput( attrs={'class': 'form-control', 'type': "text"} ),
            'message_text': forms.Textarea(
                attrs={'class': 'form-control', 'rows': "7", 'id': "comment-text-input", 'cols': "80"} ),

        }
