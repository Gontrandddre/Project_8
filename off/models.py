#!/usr/bin/python3
# -*- coding: Utf-8 -*

from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Product(models.Model):
    off_id = models.BigIntegerField(_('id'), null=True)
    name = models.CharField(_('nom'), max_length=200, null=True)
    picture = models.URLField(_('image'), null=True)
    proteins = models.CharField(_('protéines'), max_length=200, null=True)
    salt = models.CharField(_('sel'), max_length=200, null=True)
    fat = models.CharField(_('matières grasses'), max_length=200, null=True)
    sugars = models.CharField(_('sucres'), max_length=200, null=True)
    carbohydrates = models.CharField(_('glucides'), max_length=200, null=True)
    nutriscore_grade = models.CharField(_('nutriscore'),
                                        max_length=2,
                                        null=True)
    category = models.CharField(_('catégorie'), max_length=200, null=True)
    url = models.URLField(_('fiche OpenFoodFacts'), null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True)

    def __str__(self):
        return self.name
