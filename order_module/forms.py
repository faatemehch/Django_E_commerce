from django import forms
from .models import Province, City, Order


class CompleteForm( forms.ModelForm ):
    class Meta:
        model = Order
        fields = (
            'name',
            'family',
            'phone_number',
            'post_code',
            'province',
            'city',
            'address',
            'description'
        )

        widgets = {
            'name': forms.TextInput( attrs={'class': 'form-control mb-3'} ),
            'family': forms.TextInput( attrs={'class': 'form-control mb-3'} ),
            'post_code': forms.NumberInput( attrs={'class': 'form-control mb-3'} ),
            'phone_number': forms.NumberInput( attrs={'class': 'form-control mb-3'} ),
            'province': forms.Select( attrs={'class': 'form-control mb-3', 'id': 'province'} ),
            'city': forms.Select( attrs={'class': 'form-control mb-3', 'id': 'city'} ),
            'address': forms.Textarea( attrs={'class': 'form-control mb-3', 'row': '3'} ),
            'description': forms.Textarea( attrs={'class': 'form-control mb-3', 'row': '3'} )

        }

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        self.fields['city'].queryset = City.objects.none()
        self.fields['description'].required = False

        if 'province' in self.data:
            try:
                province_id = int( self.data.get( 'province' ) )
                self.fields['city'].queryset = City.objects.filter( province_id=province_id ).order_by(
                    'city_name' )
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.province.city_set.order_by( 'city_name' )
