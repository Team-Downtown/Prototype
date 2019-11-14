from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MarketUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = MarketUser
        fields = UserCreationForm.Meta.fields + ('email','phoneNumber','image','bio')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MarketUser
        fields = UserCreationForm.Meta.fields + ('email','phoneNumber','image','bio')
