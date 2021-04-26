#!/usr/bin/python3
# -*- coding: Utf-8 -*

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
import time

from ..models import Product, CustomUser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from django.conf import settings

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1920x1080')

# Create your tests here.

class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com',
                                        password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


class StaticPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@mail.com',
                                                   password='test')
        self.client.login(email='test@mail.com',
                          password='test')

        Product.objects.create(name="test_product", id=1)

        session = self.client.session
        session['search'] = 'test'
        session['input_user'] = 'test'
        session.save()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'off/index.html')
        self.assertEqual(response.resolver_match.func.__name__, 'index')
        self.assertIn('Du gras, oui, mais de qualité', response.content.decode('utf8'))

    def test_contact_page(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'off/contact.html')
        self.assertEqual(response.resolver_match.func.__name__, 'TemplateView')
        self.assertIn('Contactez-nous !', response.content.decode('utf8'))

    def test_legalNotice_page(self):
        response = self.client.get('/mentions-legales')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'off/legal_notices.html')
        self.assertEqual(response.resolver_match.func.__name__, 'TemplateView')
        self.assertIn('Mentions légales', response.content.decode('utf8'))

    def test_account(self):
        response = self.client.get('/mon-compte')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'off/account.html')
        self.assertEqual(response.resolver_match.func.__name__, 'account')
        self.assertIn('Compte', response.content.decode('utf8'))

    def test_signUp_page(self):
        response = self.client.get('/inscription')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertEqual(response.resolver_match.func.__name__, 'register')
        self.assertIn('Inscription', response.content.decode('utf8'))

    def test_signIn_page(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(response.resolver_match.func.__name__, 'LoginView')
        self.assertIn('Connexion', response.content.decode('utf8'))

    def test_logOut_page(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logged_out.html')
        self.assertEqual(response.resolver_match.func.__name__, 'LogoutView')
        self.assertIn('Déconnexion', response.content.decode('utf8'))

    def test_results_page(self):
        response = self.client.get('/resultats')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'off/results.html')
        self.assertEqual(response.resolver_match.func.__name__, 'results')
        self.assertIs(False, response.context['error_message_empty'])
        self.assertIn('Résultats', response.content.decode('utf8'))

    def test_savedProducts_page(self):
        response = self.client.get('/mes-produits')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'off/saved.html')
        self.assertEqual(response.resolver_match.func.__name__, 'saved_products')
        self.assertIn('Mes aliments sauvegardés', response.content.decode('utf8'))


class LogInPageTestCase(TestCase):

    def test_logIn_page(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@mail.com',
                                                   password='test')
        self.client.login(email='test@mail.com',
                          password='test')
        self.assertIn('_auth_user_id', self.client.session)


class LogOutPageTestCase(TestCase):

    def test_logOut_page(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@mail.com',
                                                   password='test')
        self.client.login(email='test@mail.com',
                          password='test')
        self.client.logout()
        self.assertNotIn('_auth_user_id', self.client.session)


class ApiOffTestCase(TestCase):
    pass


class Error404TestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@mail.com',
                                                   password='test')
        self.client.login(email='test@mail.com',
                          password='test')
        Product.objects.create(name="test produit", id=2)

    def test_product_page(self):
        response = self.client.get('/produit/999999999999999999999')
        self.assertEqual(response.status_code, 404)


class SessionTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@mail.com',
                                                   password='test')
        self.client.login(email='test@mail.com',
                          password='test')

    def test_results_page(self):
        response = self.client.get('/results')
        session = self.client.session
        session['search'] = 'test'
        session.save()
        self.assertEqual(session["search"], "test")

