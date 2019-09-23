# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import MarketUser

class MarketUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MarketUser

    fieldsets = UserAdmin.fieldsets + (
        ("Marketplace fields", {'fields': ('phoneNumber','image','bio',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Marketplace fields', {'fields': ('phoneNumber','image','bio',)}),
    )

admin.site.register(MarketUser, MarketUserAdmin)
