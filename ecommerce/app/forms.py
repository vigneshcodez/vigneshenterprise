from django import forms
from .models import Address

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('address_line1', 'address_line2', 'city', 'postal_code')
        widgets = {
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'door number and street'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'area name'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postal code'}),
            }
