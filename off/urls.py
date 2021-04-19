#!/usr/bin/python3
# -*- coding: Utf-8 -*

from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

app_name = "off"

urlpatterns = [
    path('', views.index, name='index'),
    path('resultats', views.results, name='results'),
    path('mes-produits', views.saved_products, name='saved-products'),
    re_path(r'^produit/(?P<id_product>[^/]+)$', views.product, name='product'),
    path('mon-compte', views.account, name='account'),
    path('mentions-legales', TemplateView.as_view(template_name="off/legal_notices.html"), name="legal-notices"),
    path('contact', TemplateView.as_view(template_name="off/contact.html"), name="contact")
]

urlpatterns += [
    path('inscription', views.register, name='register'),
]
