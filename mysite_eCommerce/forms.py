from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import Customer,ShippingAddress
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model =User
        fields = ['username', 'email', 'password1' , 'password2' , 'first_name', 'last_name']

class Customerform(ModelForm):
    class Meta:
        model = Customer
        fields = ['mobile_no', 'alter_mobile' ]

class shippingform(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['Addressline1','Addressline2','City','State','Zipcode','Country']

class edituserform(UserChangeForm):


    class Meta:
        model =User
        fields = [ 'email' , 'first_name', 'last_name']
        widgets = {'email': forms.TextInput(attrs={'readonly': 'readonly'})}