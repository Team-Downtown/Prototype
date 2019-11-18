from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MarketUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = MarketUser
        fields = ('username','first_name','last_name','email','phoneNumber','image','bio')
        labels = {
            'phoneNumber':'Phone Number',
            'bio':'Biographical Information',
        }

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MarketUser
        fields = ('first_name','last_name','email','phoneNumber','image','bio')
        labels = {
            'phoneNumber':'Phone number',
            'bio':'Biographical Information',
        }

