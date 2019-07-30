from django import forms
from django_countries.fields import CountryField

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class CheckoutForms(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'your first name',
        'class': 'checkout_input'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'your last name',
        'class': 'checkout_input'
    }))
    country = CountryField(blank_label='(select country)').formfield()
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '123 Main st',
        'class': 'checkout_input'
    }))
    zipcode = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': '1216',
        'class': 'checkout_input'
    }))
    # city = forms.CharField(widget=forms.TextInput(attrs={
    #     'placeholder': 'Tokyo',
    #     'class': 'checkout_input'
    # }))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': '01762509605',
        'class': 'checkout_input'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'yourname@mail.com',
        'class': 'checkout_input'
    }))
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES
    )
