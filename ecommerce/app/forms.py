from django import forms
from .models import Address

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('address_line1', 'address_line2', 'city', 'postal_code')
        widgets = {
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address line 1'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address line 2'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postal code'}),
            }
