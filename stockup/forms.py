from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Inventory, Sales
from django.forms import ModelForm


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["business_name", "email", "username"]

class LoginForm(AuthenticationForm):
    pass


class IventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = [
            "product_name","quantity","price","category","is_low_stock"
        ]

        widgets = {
                "product_name": forms.TextInput(attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Samsung Galaxy A15"
                }),
                "category": forms.Select(attrs={
                    "class": "form-select"
                }),
                "price": forms.NumberInput(attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "min": "0",
                    "step": "0.01"
                }),
                "quantity": forms.NumberInput(attrs={
                    "class": "form-control",
                    "placeholder": "0",
                    "min": "0",
                    "step": "1"
                }),
                "is_low_stock": forms.NumberInput(attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 5",
                    "min": "0",
                    "step": "1"
                }),
            }     



class MakeSale(forms.ModelForm):
    class Meta:
        model = Sales
        fields = [
            'quantity'
        ]


class editForm(forms.ModelForm):
    class Meta:
        model =Inventory
        fields = [
             "product_name","quantity","price","category","is_low_stock"
        ]

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity    


    def clean_price(self):
            price = self.cleaned_data['price']
            if price < 0:
                raise forms.ValidationError("Price cannot be negative.")
            return price    
    


class RecordSaleForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Inventory.objects.none()
    )

    class Meta:
        model = Sales
        fields = ["product", "quantity"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["product"].queryset = Inventory.objects.filter(
                owner=user,
                is_active=True
            )