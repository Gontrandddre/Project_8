#!/usr/bin/python3
# -*- coding: Utf-8 -*

from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email",)
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control"}),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class AuthenticationFormApp(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass
