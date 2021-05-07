from django.urls import reverse
import time

from ..models import Product, CustomUser

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from django.conf import settings

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920x1080")


class testSelenium(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(
            executable_path=str(
                settings.BASE_DIR / "webdrivers" / "chromedriver"
            ),
            options=chrome_options,
        )
        self.browser.implicitly_wait(10)
        self.browser.maximize_window()

        CustomUser.objects.create_user(
            email="testSelenium@test.test", password="testSelenium"
        )

        Product.objects.create(id=12345, off_id=678910, name="jambon")

    def tearDown(self):
        self.browser.close()

    def test_1_wrong_login_selenium(self):
        self.browser.get(self.live_server_url + reverse("login"))

        self.browser.find_element_by_id("emailLogin").send_keys(
            "testSelenium@test.test"
        )
        self.browser.find_element_by_id("passwordLogin").send_keys("ferfqerqsfqezrf")
        self.browser.find_element_by_id("submitLogin").click()

        self.assertEqual(
            self.browser.find_element_by_id("alert_login").text,
            "Votre email ou votre mot de passe est incorrect. Veuillez réessayer.",
        )

    def test_2_sign_up_selenium(self):
        self.browser.get(self.live_server_url)
        sign_up = self.browser.find_element_by_id("signUp")
        sign_up.click()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse("off:register")
        )

    def test_3_login_selenium(self):
        self.browser.get(self.live_server_url + reverse("login"))

        self.browser.find_element_by_id("emailLogin").send_keys(
            "testSelenium@test.test"
        )
        self.browser.find_element_by_id("submitLogin").send_keys("zerty51FC")
        self.browser.find_element_by_id("passwordLogin").click()

    def test_4_index_selenium(self):
        self.browser.get(self.live_server_url + reverse("login"))

        self.browser.find_element_by_id("emailLogin").send_keys(
            "testSelenium@test.test"
        )
        self.browser.find_element_by_id("passwordLogin")\
                    .send_keys("testSelenium")
        self.browser.find_element_by_id("submitLogin").submit()

        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse("off:index")
        )

    def test_5_search_product_index(self):

        self.browser.get(self.live_server_url + reverse("login"))

        self.browser.find_element_by_id("emailLogin").send_keys(
            "testSelenium@test.test"
        )
        self.browser.find_element_by_id("passwordLogin")\
                    .send_keys("testSelenium")
        self.browser.find_element_by_id("submitLogin").submit()

        time.sleep(2)

        self.browser.find_element_by_id("querySearch").send_keys("jambon")
        self.browser.find_element_by_id("submitQuery").submit()

        time.sleep(2)

        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse("off:results")
        )

    def test_6_save_product_selenium(self):

        self.browser.get(self.live_server_url + reverse("login"))

        self.browser.find_element_by_id("emailLogin").send_keys(
            "testSelenium@test.test"
        )
        self.browser.find_element_by_id("passwordLogin")\
                    .send_keys("testSelenium")
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
            self.live_server_url + reverse("off:saved-products"),
        )
        self.assertEqual(
            "product-saved-" + str(Product.objects.get(id=12345).id),
            productSaved.get_attribute("id"),
        )

    def test_7_logout_selenium(self):
        self.browser.get(self.live_server_url + reverse("login"))

        self.browser.find_element_by_id("emailLogin").send_keys(
            "testSelenium@test.test"
        )
        self.browser.find_element_by_id("passwordLogin")\
                    .send_keys("testSelenium")
        self.browser.find_element_by_id("submitLogin").submit()

        time.sleep(1)

        self.browser.find_element_by_id("logoutLink").click()
        time.sleep(1)

        self.assertEqual(
            self.browser.find_element_by_id("logoutAlert").text, "DÉCONNEXION"
        )


class NewFeatureSelenium(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome(
            executable_path=str(
                settings.BASE_DIR / "webdrivers" / "chromedriver"
            ),
            options=chrome_options,
        )
        self.browser.implicitly_wait(10)
        self.browser.maximize_window()

        CustomUser.objects.create_user(
            email="testSelenium2@test.test", password="testSelenium2"
        )

        Product.objects.create(id=12345, off_id=678910, name="jambon")

    def tearDown(self):
        self.browser.close()
    
    def test_change_password_selenium(self):
        self.browser.get(self.live_server_url + reverse("login"))

        self.browser.find_element_by_id("emailLogin").send_keys(
            "testSelenium2@test.test"
        )
        self.browser.find_element_by_id("passwordLogin")\
                    .send_keys("testSelenium2")
        self.browser.find_element_by_id("submitLogin").submit()
        
        current_user_old = CustomUser.objects.get(email='testSelenium2@test.test')
        current_user_old_password = current_user_old.password

        time.sleep(1)

        self.browser.get(self.live_server_url + reverse("off:change-password"))
        
        time.sleep(1)

        self.browser.find_element_by_id("id_old_password").send_keys(
            "testSelenium2"
        )
        self.browser.find_element_by_id("id_new_password1")\
                    .send_keys("NewPasswordSelenium")
        self.browser.find_element_by_id("id_new_password2")\
                    .send_keys("NewPasswordSelenium")
        self.browser.find_element_by_id("submitChangePassword").submit()

        time.sleep(1)

        current_user_new = CustomUser.objects.get(email='testSelenium2@test.test')
        current_user_new_password = current_user_new.password

        time.sleep(1)

        self.assertEqual(
            self.browser.find_element_by_id("messageSuccess").text, "Votre mot de passe a bien été modifié."
        )
        self.assertNotEqual(
            current_user_new_password, current_user_old_password
        )
