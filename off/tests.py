#!/usr/bin/python3
# -*- coding: Utf-8 -*

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
import time

from .models import Product, CustomUser

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

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


# class StaticPageTest(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.user = CustomUser.objects.create_user(email='test@mail.com',
#                                                    password='test')
#         self.client.login(email='test@mail.com',
#                           password='test')

#         Product.objects.create(name="test_product", id=1)

#         session = self.client.session
#         session['search'] = 'test'
#         session['input_user'] = 'test'
#         session.save()

#     def test_index_page(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'off/index.html')
#         self.assertEqual(response.resolver_match.func.__name__, 'index')
#         self.assertIn('Du gras, oui, mais de qualité', response.content.decode('utf8'))

#     def test_contact_page(self):
#         response = self.client.get('/contact')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'off/contact.html')
#         self.assertEqual(response.resolver_match.func.__name__, 'TemplateView')
#         self.assertIn('Contactez-nous !', response.content.decode('utf8'))

#     def test_legalNotice_page(self):
#         response = self.client.get('/mentions-legales')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'off/legal_notices.html')
#         self.assertEqual(response.resolver_match.func.__name__, 'TemplateView')
#         self.assertIn('Mentions légales', response.content.decode('utf8'))

#     def test_account(self):
#         response = self.client.get('/mon-compte')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'off/account.html')
#         self.assertEqual(response.resolver_match.func.__name__, 'account')
#         self.assertIn('Compte', response.content.decode('utf8'))

#     def test_signUp_page(self):
#         response = self.client.get('/inscription')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/register.html')
#         self.assertEqual(response.resolver_match.func.__name__, 'register')
#         self.assertIn('Inscription', response.content.decode('utf8'))

#     def test_signIn_page(self):
#         response = self.client.get('/accounts/login/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/login.html')
#         self.assertEqual(response.resolver_match.func.__name__, 'LoginView')
#         self.assertIn('Connexion', response.content.decode('utf8'))

#     def test_logOut_page(self):
#         response = self.client.get('/accounts/logout/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/logged_out.html')
#         self.assertEqual(response.resolver_match.func.__name__, 'LogoutView')
#         self.assertIn('Déconnexion', response.content.decode('utf8'))

#     def test_results_page(self):
#         response = self.client.get('/resultats')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'off/results.html')
#         self.assertEqual(response.resolver_match.func.__name__, 'results')
#         self.assertIs(False, response.context['error_message_empty'])
#         self.assertIn('Résultats', response.content.decode('utf8'))

#     def test_savedProducts_page(self):
#         response = self.client.get('/mes-produits')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'off/saved.html')
#         self.assertEqual(response.resolver_match.func.__name__, 'saved_products')
#         self.assertIn('Mes aliments sauvegardés', response.content.decode('utf8'))


# class DatabaseTestCase(TestCase):

#     def setUp(self):
#         pass

#     def test_categories_products_objects(self):
#         # products = Product.objects.all()
#         # list_categories = []
#         # for product in products:
#         #     if not product.category in categories:
#         #         categories.append(product.category)
#         #     else:
#         #         continue

#         # self.assertEqual(len(list_categories), 10)
#         pass

#     def test_customUser_objects(self):
#         pass


# class SignUpPageTestCase(TestCase):
#     pass


# # class SignInPageTestCase(TestCase):

# #     def test_SignIn_page(self):
# #         response = self.client.post({'email': 'test2@mail.com',
# #                                      'password1': 'test2',
# #                                      'passwword2': 'test2'})

# #         self.assertIn('_auth_user_id', self.client.session)


# class LogInPageTestCase(TestCase):

#     def test_logIn_page(self):
#         self.client = Client()
#         self.user = CustomUser.objects.create_user(email='test@mail.com',
#                                                    password='test')
#         self.client.login(email='test@mail.com',
#                           password='test')
#         self.assertIn('_auth_user_id', self.client.session)


# class LogOutPageTestCase(TestCase):

#     def test_logOut_page(self):
#         self.client = Client()
#         self.user = CustomUser.objects.create_user(email='test@mail.com',
#                                                    password='test')
#         self.client.login(email='test@mail.com',
#                           password='test')
#         self.client.logout()
#         self.assertNotIn('_auth_user_id', self.client.session)


# class ApiOffTestCase(TestCase):
#     pass


# class ListSubsituteProductsTestCase(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.user = CustomUser.objects.create_user(email='test@mail.com',
#                                                    password='test')
#         self.client.login(email='test@mail.com',
#                           password='test')

#         Product.objects.create(name="jambon de Paris", id=1)

#     def test_results_page(self):
#         response = self.client.post('/results', {'query': 'jambon'})
#         print(response.wsgi_request)
#         self.assertEqual(response.request['REQUEST_METHOD'], "POST")
#         self.assertIn('jambon', response.content.decode('utf8'))


# class ListSavedProductTestCase(TestCase):
#     pass


# class QueryTestCase(TestCase):
#     pass


# class SaveProductTestCase(TestCase):
#     pass


# class VisualizeProductPageTestCase(TestCase):
#     pass


# class Error404TestCase(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.user = CustomUser.objects.create_user(email='test@mail.com',
#                                                    password='test')
#         self.client.login(email='test@mail.com',
#                           password='test')
#         Product.objects.create(name="test produit", id=2)

#     def test_product_page(self):
#         response = self.client.get('/produit/999999999999999999999')
#         self.assertEqual(response.status_code, 404)


# class ViewWithOutLogin(TestCase):

#     # def test_index_page(self):

#     #     response = self.client.get('/')
#     #     self.assertEqual(response.status_code, )
#     #     self.assertTemplateUsed(response, 'registration/login.html')
#     #     self.assertEqual(response.resolver_match.func.__name__, 'LoginView')
#     #     self.assertIn('Veuillez vous connecter pour visualiser cette page', response.content.decode('utf8'))

#     # def test_contact_page(self):

#     # def test_legalNotice_page(self):

#     # def test_account(self):

#     # def test_signUp_page(self):

#     # def test_signIn_page(self):

#     # def test_logOut_page(self):

#     # def test_savedProducts_page(self):

#     pass


# class SessionTestCase(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.user = CustomUser.objects.create_user(email='test@mail.com',
#                                                    password='test')
#         self.client.login(email='test@mail.com',
#                           password='test')

#     def test_results_page(self):
#         response = self.client.get('/results')
#         session = self.client.session
#         session['search'] = 'test'
#         session.save()
#         self.assertEqual(session["search"], "test")


class testSelenium(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('chromedriver')
    
    def tearDown(self):
        self.browser.close()

    def test_wrong_login_selenium(self):
        self.browser.get(self.live_server_url)
        
        email = self.browser.find_element_by_id("email_login")
        submit = self.browser.find_element_by_id("submit_login")
        password = self.browser.find_element_by_id("password_login")
        
        email.send_keys("gontrand.daudre@kelindi.com")
        password.send_keys("zerty51FC")
        submit.click()
        alert = self.browser.find_element_by_id("alert_login")
        self.assertEqual(
            alert.text, "Veuillez vous connecter pour visualiser cette page."
        )
        
    def test_login_selenium(self):
        self.browser.get(self.live_server_url)
        
        email = self.browser.find_element_by_id("email_login")
        submit = self.browser.find_element_by_id("submit_login")
        password = self.browser.find_element_by_id("password_login")
        
        email.send_keys("gontrand.daudre@kelindi.com")
        password.send_keys("azerty51FC")
        submit.click()

#     def test_index_selenium(self):
#         self.browser.get(self.live_server_url)
#         add_url = self.live_server_url + reverse("off:index")
#         self.assertEqual(
#             self.browser.current_url,
#             add_url
#         )
#         time.sleep(5)


        

        