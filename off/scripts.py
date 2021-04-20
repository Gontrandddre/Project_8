#!/usr/bin/python3
# -*- coding: Utf-8 -*

from .constantes import (
    CATEGORIES, URL_BEGIN, NO_CHARS_LIST, STOP_WORDS,
)
from .models import Product, CustomUser
import requests 

def update_database():

    for cat_name in CATEGORIES:
        params_url = {'action': 'process',
                    'tagtype_0': 'categories',
                    'tag_contains_0': 'contains',
                    'tag_0': cat_name,
                    'sort_by': 'unique_scans_n',
                    'page_size': 1000,
                    'axis_x': 'energy',
                    'axis_y': 'products_n',
                    'json': '1'}

        response = requests.get(URL_BEGIN, params=params_url)
        response_json = response.json()

        for product in response_json['products']:
            try:
                name = product['product_name_fr']
            except KeyError:
                break
            try:
                picture = product['image_url']
            except KeyError:
                break
            try:
                off_id = product['id']
            except KeyError:
                break
            try:
                nutriscore_grade = product['nutriscore_grade']
            except KeyError:
                break
            try:
                proteins = product['nutriments']['proteins']
            except KeyError:
                break
            try:
                salt = product['nutriments']['salt']
            except KeyError:
                break
            try:
                fat = product['nutriments']['fat']
            except KeyError:
                break
            try:
                sugars = product['nutriments']['sugars']
            except KeyError:
                break
            try:
                carbohydrates = product['nutriments']['carbohydrates']
            except KeyError:
                break
            try:
                url = product['url']
            except KeyError:
                break
            category = cat_name

            Product.objects.update_or_create(
                defaults={'off_id': off_id},
                name=name,
                picture=picture,
                proteins=proteins,
                salt=salt,
                fat=fat,
                sugars=sugars,
                carbohydrates=carbohydrates,
                nutriscore_grade=nutriscore_grade,
                category=category,
                url=url,
            )
