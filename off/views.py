#!/usr/bin/python3
# -*- coding: Utf-8 -*

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Product, CustomUser
from .forms import CustomUserCreationForm, AuthenticationFormApp
from .constantes import (
    CATEGORIES, URL_BEGIN, NO_CHARS_LIST, STOP_WORDS,
)

import requests
from unidecode import unidecode

# Create your views here.


def register(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password == password2:
                user = authenticate(email=email, password=password)

                if user is not None:
                    auth_login(request, user)
                    return redirect('off:index')
            else:
                form = CustomUserCreationForm()

        else:
            form = CustomUserCreationForm()

    if request.method == "GET":
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('off:index')

    if request.method == 'GET':

        form = AuthenticationFormApp()
        return render(request, 'registration/login.html', {'form': form})

    if request.method == 'POST':
        form = AuthenticationFormApp(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('off:index')
        else:
            print('User not found')
    else:
        return render(request, 'login_error.html', {'form': form})


@login_required(login_url='login')
def index(request):

    error_message_empty = False
    error_message_wrong = False

    if request.method == "POST":

        if not request.POST.get('query'):
            error_message_empty = True

        else:
            input_brut = request.POST.get('query')
            input_withoutCharsSpe = input_brut.translate(
                {ord(c): " " for c in NO_CHARS_LIST}
            )
            input_no_accent = unidecode(input_withoutCharsSpe)
            input_split = input_no_accent.split()

            for element in input_split:
                if element in STOP_WORDS:
                    input_split.remove(element)

            if not input_split:
                error_message_wrong = True

            else:
                request.session['search'] = input_split
                request.session['input_user'] = input_brut
                return redirect('off:results')

    if request.method == 'GET':

        if Product.objects.count() == 0:

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

                    Product.objects.create(
                        off_id=off_id,
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

        else:
            pass

    return render(request, 'off/index.html', {
        "error_message_empty": error_message_empty,
        "error_message_wrong": error_message_wrong,
      })


@login_required(login_url='login')
def results(request):

    error_message_empty = False
    error_message_no_results = False
    list_saved_id_products = []

    if request.method == "POST":

        # new query (header)
        if request.POST.get('query'):

            request.session['input_user'] = request.POST.get('query')
            input_brut = request.POST.get('query')
            input_withoutCharsSpe = input_brut.translate(
                {ord(c): " " for c in NO_CHARS_LIST}
            )
            input_no_accent = unidecode(input_withoutCharsSpe)
            input_split = input_no_accent.split()

            for element in input_split:
                if element in STOP_WORDS:
                    input_split.remove(element)

            if not input_split:
                error_message_empty = True

            else:
                request.session['search'] = input_split

        # details product
        if request.POST.get('product'):
            return redirect('off:product', request.POST.get('product'))

        # save product
        if request.POST.get('save'):
            current_user = request.user
            product = get_object_or_404(Product, pk=request.POST.get('save'))
            user = get_object_or_404(CustomUser, pk=current_user.id)
            user.product_set.add(product)

            for element in user.product_set.all():
                list_saved_id_products.append(element.id)

    if request.method == "GET":

        current_user = request.user
        user = get_object_or_404(CustomUser, pk=current_user.id)

        for element in user.product_set.all():
            list_saved_id_products.append(element.id)

    input_split = request.session['search']
    input_user = request.session['input_user']

    categories_products = []
    for word in input_split:
        for product in Product.objects.filter(name__icontains=word):
            categories_products.append(product.category)

    if categories_products:
        main_category = max(set(categories_products),
                            key=categories_products.count)
        substitute_products_list = Product.objects\
            .filter(category=main_category)\
            .order_by('nutriscore_grade', 'name')[:12]
        paginator = Paginator(substitute_products_list, 6)
        page = request.GET.get('page')

        try:
            substitute_products = paginator.page(page)
        except PageNotAnInteger:
            substitute_products = paginator.page(1)
        except EmptyPage:
            substitute_products = paginator.page(paginator.num_pages)

    else:
        error_message_no_results = True
        substitute_products = None

    return render(request, 'off/results.html', {
        "error_message_empty": error_message_empty,
        "error_message_no_results": error_message_no_results,
        "input_user": input_user,
        "substitute_products": substitute_products,
        "list_saved_id_products": list_saved_id_products,
    })


@login_required(login_url='login')
def saved_products(request):

    current_user = request.user
    user = get_object_or_404(CustomUser, pk=current_user.id)
    saved_products = user.product_set.all()

    return render(request, 'off/saved.html', {
        'saved_products': saved_products,
    })


@login_required(login_url='login')
def product(request, id_product):

    list_saved_id_products = []
    current_user = request.user
    user = get_object_or_404(CustomUser, pk=current_user.id)

    if request.method == "POST":

        # new query (header)
        if request.POST.get('query'):

            request.session['input_user'] = request.POST.get('query')
            input_brut = request.POST.get('query')
            input_withoutCharsSpe = input_brut.translate(
                {ord(c): " " for c in NO_CHARS_LIST}
            )
            input_no_accent = unidecode(input_withoutCharsSpe)
            input_split = input_no_accent.split()

            for element in input_split:
                if element in STOP_WORDS:
                    input_split.remove(element)

            if not input_split:
                error_message_empty = True

            else:
                request.session['search'] = input_split

            return redirect('off:results')

        # save product
        if request.POST.get('save'):

            product = get_object_or_404(Product, pk=request.POST.get('save'))
            user.product_set.add(product)

    for element in user.product_set.all():
        list_saved_id_products.append(element.id)

    product = get_object_or_404(Product, pk=id_product)

    return render(request, 'off/product.html', {
        "product": product,
        "list_saved_id_products": list_saved_id_products,
    })


@login_required(login_url='login')
def account(request):

    current_user = request.user
    user = get_object_or_404(CustomUser, pk=current_user.id)

    return render(request, 'off/account.html', {
        "user": user,
    })
