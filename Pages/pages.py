import time
import random
from urllib.parse import urlparse, unquote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

from Pages.test_params import sorted_values
from Pages.locators import *


class MirBeer:
    """Родительский класс для некоторых классов, возвращает части URL"""
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
    """Класс для проверки авторизации и регистрации"""
    def __init__(self, driver, url):
        super().__init__(driver, url)
        driver.get(url)
        # Т.к. на сайте при открытии выводится запрос города в всплывающем окне, а headers в Селениум нет,
        # добавлены cookie
        driver.add_cookie({'name': 'icity_confirmed', 'value': '1'})
        driver.refresh()
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
    """Класс для проверки поиска по названию товара """
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.driver = driver
        self.driver.get(url)
        self.driver.add_cookie({'name': 'icity_confirmed', 'value': '1'})
        self.driver.refresh()
        self.search_field_c = self.driver.find_element(*SearchLocators.SEARCH_FIELD_CLICK)
        self.search_field = self.driver.find_element(*SearchLocators.SEARCH_FIELD)
        self.search_btn = self.driver.find_element(*SearchLocators.SEARCH_BTN)

    def enter_search_value(self, value):
        self.search_field.send_keys(value)

    def search_btn_click(self):
        self.search_btn.click()

    def search_field_click(self):
        self.search_field_c.click()

    def get_search_result(self):
        """Метод для получения результата поиска, страница выдачи прокручивается вниз,
         пока не будет найден соотв. элемент"""
        while True:
            try:
                if self.driver.find_element(*SearchLocators.SCROLL_UP):
                    break
            except NoSuchElementException:
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.PAGE_DOWN)
                actions.perform()

    def check_search(self):
        """Метод для заполнения результата поиска товарав в список"""
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        wares = soup.find_all('div', class_=SearchLocators.WARE)
        result = []
        for ware in wares:
            result.append(str(ware.find('a')).split('_blank">')[1].rstrip('</a>'))
        return result


class SortedCheck:
    """Класс для проверки сортировки"""
    def __init__(self, driver, url, sort_value):
        self.result = []
        driver.get(url)
        driver.add_cookie({'name': 'icity_confirmed', 'value': '1'})
        driver.refresh()
        self.select = driver.find_element(By.XPATH, f'//option[@value="{sort_value}"]')
        self.select.click()
        driver.refresh()
        # Если на странице еще есть элемент подгрузки новых результатов поиска,
        # то прокручиваем страницу ниже.
        while True:
            try:
                if driver.find_element(*SortedCheckLocators.LOAD_MORE):
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.PAGE_DOWN)
                    actions.perform()
                    driver.implicitly_wait(3)
            except NoSuchElementException:
                self.src = driver.page_source
                break

    def get_sorted_result(self):
        """Метод для сохранения списка отсортированных товаров в список из списков,
        наименование и цена"""
        soup = BeautifulSoup(self.src, 'lxml')
        wares_in_stock = soup.find_all('a', class_=SortedCheckLocators.WARES_CLASS)
        for ware in wares_in_stock:
            self.result.append([ware.get(SortedCheckLocators.NAME_ID), float(ware.get(SortedCheckLocators.PRICE_ID))])
        return self.result

    def check_sorted_result(self, sort_value):
        """Метод для сравнения результата сортировки на сейте,
          сортировка по цене, возрастанию и убыванию и названию"""
        result_check = self.result
        if sort_value == sorted_values[0]:
            result_check.sort(key=lambda x: x[1])
        elif sort_value == sorted_values[1]:
            result_check.sort(key=lambda x: x[1], reverse=True)
        elif sort_value == sorted_values[2]:
            result_check.sort(key=lambda x: x[0])
        return result_check


class Cart:
    """Класс для проверки добавления товара в корзину"""
    def __init__(self, driver, url):
        self.driver = driver
        self.driver.get(url)
        self.driver.add_cookie({'name': 'icity_confirmed', 'value': '1'})
        self.driver.refresh()
        # Прокручиваем страницу вниз, и ждем, пока не подгрузится товар, который можно купить
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
        """Метод возвращает цену товара, который будет добавлен в корзину"""
        self.ware.click()
        price = self.driver.find_element(*CartLocators.PRICE).text
        return price

    def put_ware_to_cart(self):
        buy_button = self.driver.find_element(*CartLocators.BUY_BTN)
        buy_button.click()

    def get_price_at_cart(self):
        """Метод возвращает цену товара в корзине"""
        price_at_cart = WebDriverWait(self.driver, 3).until(
            lambda d: d.find_element(*CartLocators.PRICE_CART))
        return str(price_at_cart.text).split('.')[0]


class FilterCheck:
    """Метод для проверки работы фильтра по цене в списке товаров, найденных по названию"""
    def __init__(self, driver, url):
        self.driver = driver
        self.driver.get(url)
        self.driver.add_cookie({'name': 'icity_confirmed', 'value': '1'})
        self.driver.refresh()
        self.driver.implicitly_wait(3)
        self.min_price = self.driver.find_element(*FilterLocators.MIN_PRICE)
        self.max_price = self.driver.find_element(*FilterLocators.MAX_PRICE)

    def enter_filter_price(self):
        """Метод берет мин. и макс. цену в списке найденных товаров. Диапазон цен разбивается на три части
        и рандомно генерируется новые мин. и макс. цена из первой и третей третей соотв.
        Новые цены возрващаются для проверки"""
        min_price_value = int(self.min_price.get_attribute('placeholder').replace("\u00A0", ''))
        max_price_value = int(self.max_price.get_attribute('placeholder').replace("\u00A0", ''))
        new_min_price = random.randint(min_price_value, (max_price_value-min_price_value)//3)
        new_max_price = random.randint(2*(max_price_value-min_price_value)//3, max_price_value)
        # Для вставки нового значения фильтра нужно кликнуть на поле фильтра, очистить содержимое,
        # вставить нужно значение и подождать, пока обновиться список товаров. Ждать нужно дважды -
        # после вставки нового мин. значения и макс.
        self.min_price.click()
        self.min_price.send_keys(Keys.CONTROL + 'a')
        self.min_price.send_keys(Keys.DELETE)
        self.min_price.send_keys(new_min_price)
        self.max_price.click()
        self.max_price.send_keys(Keys.CONTROL + 'a')
        self.max_price.send_keys(Keys.DELETE)
        time.sleep(2)
        self.max_price.send_keys(new_max_price)
        self.driver.find_element(*FilterLocators.PAGE_CLICK).click()
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()
        time.sleep(2)
        return new_min_price, new_max_price

    def get_wares_witch_filter(self):
        """Метод получае список товаров, отфильтрованных по цене"""
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        wares = soup.find_all('span', class_=FilterLocators.WARE_CLASS)
        result = []
        for ware in wares:
            result.append(ware.text.split('.')[0].replace("\u00A0", '').replace(',', '.'))
        return result
