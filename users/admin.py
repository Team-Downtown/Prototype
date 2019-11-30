# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import MarketUser
from market.admin import ExportMixinAdmin
from import_export import resources


class MarketUserResource(resources.ModelResource):
    class Meta:
        model = MarketUser
        fields = ('id', 'username', 'date_joined', 'is_active')

class MarketUserAdmin(ExportMixinAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MarketUser
    resource_class = MarketUserResource

    fieldsets = UserAdmin.fieldsets + (
        ("Marketplace fields", {'fields': ('phoneNumber','image','bio',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Marketplace fields', {'fields': ('phoneNumber','image','bio',)}),
    )

    def __str__(self):
        return self.name

admin.site.register(MarketUser, MarketUserAdmin)
