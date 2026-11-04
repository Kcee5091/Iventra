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