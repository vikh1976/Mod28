from urllib.parse import urlparse, unquote

import test_params
from locators import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


class MirBeer:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def get_relative_link(self):
        url = urlparse(self.driver.current_url)
        return url.path

    def get_url_query(self):
        url = urlparse(self.driver.current_url).query
        return unquote(url.split('&params')[0])


class AuthPage(MirBeer):
    def __init__(self, driver, url):
        super().__init__(driver, url)
        driver.get(url)
        driver.add_cookie({'name': 'icity_confirmed', 'value': '1'})
        driver.refresh()
        # создаем нужные элементы
        self.email = driver.find_element(*AuthLocators.AUTH_EMAIL)
        self.password = driver.find_element(*AuthLocators.AUTH_PASS)
        self.btn = driver.find_element(*AuthLocators.AUTH_BTN)
        self.registration = driver.find_element(*AuthLocators.REG_EMAIL)
        self.reg_btn = driver.find_element(*AuthLocators.REG_BTN)

    def enter_email(self, value):
        self.email.send_keys(value)

    def enter_pass(self, value):
        self.password.send_keys(value)

    def btn_click(self):
        self.btn.click()

    def reg_btn_click(self):
        self.reg_btn.click()

    def enter_registration_email(self, value):
        self.registration.send_keys(value)


class SearchAndMore(MirBeer):
    def __init__(self, driver, url):
        super().__init__(driver, url)
        driver.get(url)
        driver.add_cookie({'name': 'icity_confirmed', 'value': '1'})
        driver.refresh()
        self.search_field_c = driver.find_element(*SearchLocators.SEARCH_FIELD_CLICK)
        self.search_field = driver.find_element(*SearchLocators.SEARCH_FIELD)
        self.search_btn = driver.find_element(*SearchLocators.SEARCH_BTN)

    def enter_search_value(self, value):
        self.search_field.send_keys(value)

    def search_btn_click(self):
        self.search_btn.click()

    def search_field_click(self):
        self.search_field_c.click()


class SortedCheck(MirBeer):
    def __init__(self, driver, url, sort_value):
        super().__init__(driver, url)
        self.result = []
        driver.get(url)
        driver.add_cookie({'name': 'icity_confirmed', 'value': '1'})
        driver.refresh()
        self.select = driver.find_element(By.XPATH, f'//option[@value="{sort_value}"]')
        self.select.click()
        driver.refresh()
        try:
            while True:
                if not driver.find_element(*SortedCheckLocators.LOAD_MORE):
                    break
                else:
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.PAGE_DOWN)
                    actions.perform()
                    driver.implicitly_wait(3)
        except NoSuchElementException:
            self.src = driver.page_source

    def get_sorted_result(self):
        soup = BeautifulSoup(self.src, 'lxml')
        wares_in_stock = soup.find_all('a', class_=SortedCheckLocators.WARES_CLASS)
        for ware in wares_in_stock:
            self.result.append([ware.get(SortedCheckLocators.NAME_ID), float(ware.get(SortedCheckLocators.PRICE_ID))])
        return self.result

    def check_sorted_result(self, sort_value):
        result_check = self.result
        if sort_value == test_params.sorted_values[0]:
            result_check.sort(key=lambda x: x[1])
        elif sort_value == test_params.sorted_values[1]:
            result_check.sort(key=lambda x: x[1], reverse=True)
        elif sort_value == test_params.sorted_values[2]:
            result_check.sort(key=lambda x: x[0])
        return result_check


class Cart(MirBeer):
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.driver = driver
        self.driver.get(url)
        self.driver.add_cookie({'name': 'icity_confirmed', 'value': '1'})
        self. driver.refresh()
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()
        while True:
            try:
                self.ware = WebDriverWait(driver, 3).until(lambda d: d.find_element(*CartLocators.WARE))
                break
            except NoSuchElementException as ex:
                print(f'Still wait...{ex}')

    def get_ware_price(self):
        self.ware.click()
        price = self.driver.find_element(*CartLocators.PRICE).text
        return price

    def put_ware_to_cart(self):
        buy_button = self.driver.find_element(*CartLocators.BUY_BTN)
        buy_button.click()

    def get_price_at_cart(self):
        price_at_cart = WebDriverWait(self.driver, 3).until(
            lambda d: d.find_element(*CartLocators.PRICE_CART))
        return str(price_at_cart.text).split('.')[0]
