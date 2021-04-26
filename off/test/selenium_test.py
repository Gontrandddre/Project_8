from django.test import TestCase, Client
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


class testSelenium(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(
            executable_path=str(settings.BASE_DIR / 'webdrivers' / 'chromedriver'),
            options=chrome_options,
        )
        self.browser.implicitly_wait(10)
        self.browser.maximize_window()
        
        CustomUser.objects.create_user(
            email='testSelenium@test.test',
            password='testSelenium'
        )

        Product.objects.create(
            id=12345,
            off_id=678910,
            name='jambon'                        
        )
    
    def tearDown(self):
        self.browser.close()

    def test_wrong_login_selenium(self):
        self.browser.get(self.live_server_url)
        
        self.browser.find_element_by_id("emailLogin").send_keys("testSelenium@test.test")
        self.browser.find_element_by_id("passwordLogin").send_keys("zerty51FC")
        self.browser.find_element_by_id("submitLogin").click()
          
        self.assertEqual(
            self.browser.find_element_by_id("alert_login").text,
            "Veuillez vous connecter pour visualiser cette page."
        )
        
    def test_login_selenium(self):
        self.browser.get(self.live_server_url)
        
        self.browser.find_element_by_id("emailLogin").send_keys("testSelenium@test.test")
        self.browser.find_element_by_id("submitLogin").send_keys("zerty51FC")
        self.browser.find_element_by_id("passwordLogin").click()
    
    def test_sign_up_selenium(self):
        self.browser.get(self.live_server_url)
        sign_up = self.browser.find_element_by_id("signUp")
        sign_up.click()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse("off:register")
        )
    
    def test_index_selenium(self):
        self.browser.get(self.live_server_url)
        
        self.browser.find_element_by_id("emailLogin").send_keys("testSelenium@test.test")
        self.browser.find_element_by_id("passwordLogin").send_keys("testSelenium")
        self.browser.find_element_by_id("submitLogin").submit()
        
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse("off:index")
        )

    def test_search_product_index(self):

        self.browser.get(self.live_server_url + reverse("off:index"))

        self.browser.find_element_by_id("emailLogin").send_keys("testSelenium@test.test")
        self.browser.find_element_by_id("passwordLogin").send_keys("testSelenium")
        self.browser.find_element_by_id("submitLogin").submit()

        time.sleep(2)
        
        self.browser.find_element_by_id("querySearch").send_keys("jambon")
        self.browser.find_element_by_id("submitQuery").submit()

        time.sleep(2)

        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse("off:results")
        )
        
    def test_save_product_selenium(self):
        
        self.browser.get(self.live_server_url + reverse("off:index"))

        self.browser.find_element_by_id("emailLogin").send_keys("testSelenium@test.test")
        self.browser.find_element_by_id("passwordLogin").send_keys("testSelenium")
        self.browser.find_element_by_id("submitLogin").submit()
        
        time.sleep(1)
        
        self.browser.find_element_by_id("querySearch").send_keys("jambon")
        self.browser.find_element_by_id("submitQuery").submit()

        time.sleep(1)

        self.browser.find_element_by_id("save-12345").submit()

        time.sleep(1)

        self.browser.find_element_by_id("savedProductsLink").click()

        time.sleep(1)

        productSaved = self.browser.find_element_by_id("product-saved-12345")

        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse("off:saved-products")
        )
        self.assertEqual(
            'product-saved-' + str(Product.objects.get(id=12345).id),
            productSaved.get_attribute('id')
        )

    def test_logout_selenium(self):
        self.browser.get(self.live_server_url + reverse("off:index"))

        self.browser.find_element_by_id("emailLogin").send_keys("testSelenium@test.test")
        self.browser.find_element_by_id("passwordLogin").send_keys("testSelenium")
        self.browser.find_element_by_id("submitLogin").submit()
        
        time.sleep(1)

        self.browser.find_element_by_id("logoutLink").click()
        time.sleep(1)

        self.assertEqual(
            self.browser.find_element_by_id("logoutAlert").text,
            "Déconnexion"
        )