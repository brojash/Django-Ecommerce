from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):

	shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre'}), required=True)
	shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}), required=True)
	shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Direccion 1'}), required=True)
	shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Direccion 2'}), required=True)
	shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ciudad'}), required=True)
	shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Region'}), required=False)
	shipping_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Codigo postal'}), required=False)
	shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Pais'}), required=True)

	class Meta:
		model = ShippingAddress
		fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']

		exclude = ['user',]

class PaymentForm(forms.Form):
	card_name =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de titular'}), required=True)
	card_number =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numero tarjeta'}), required=True)
	card_exp_date =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Fecha de vencimiento'}), required=True)
	card_cvv_number =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV'}), required=True)
	card_address1 =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Direccion 1'}), required=True)
	card_address2 =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Direccion 2'}), required=False)
	card_city =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ciudad'}), required=True)
	card_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Region'}), required=True)
	card_zipcode =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Codigo postal'}), required=True)
	card_country =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Pais'}), required=True)