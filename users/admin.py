from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm()

    list_display = ["email", "name", "is_active", "is_staff"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Персональная информация", {"fields": ["name"]}),
        ("Права", {"fields": ["is_active", "is_staff"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classses": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        )
    ]

    search_fields = ["email", "name"]
    ordering = ["email", "name"]


admin.site.register(CustomUser, UserAdmin)
