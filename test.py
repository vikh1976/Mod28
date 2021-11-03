import pytest
import pytest_check as check

# Тесты: логин(негативные - цифры, символы, иероглиф, кириллица, 255 символов, пустое)
# пароль(негативные - цифры, символы, иероглиф, кириллица, 255 символов, пустое)
# регистрация (негативные - цифры, символы, иероглиф, кириллица, 255 символов, пустое)
# поиск (негативные - цифры, символы, иероглиф, кириллица, 100 символов, пустое)
# правильный логин и пароль, регистация с правильной почтой
# сортировка - по возрастанию, убыванию, название.
# Добавление товара в корзину
# Поиск товара по названию.
# Фильтр по цене.
from Pages.pages import AuthPage, SearchAndMore, SortedCheck, Cart, FilterCheck
from Pages.test_params import *


@pytest.mark.negative
@pytest.mark.parametrize('email_t', neg_email)
@pytest.mark.parametrize('password_t', neg_password)
def test_login_password_neg(selenium, email_t, password_t):
    """Тест ввода логина и пароля"""
    page = AuthPage(selenium, auth_url)
    page.enter_email(email_t)
    page.enter_pass(password_t)
    page.btn_click()
    assert page.get_relative_link() != '/profile/orders/all/'


@pytest.mark.negative
@pytest.mark.parametrize('email_t', neg_email)
def test_register_neg(selenium, email_t):
    """Тест регистрации с неправильной почтой"""
    page = AuthPage(selenium, auth_url)
    page.enter_registration_email(email)
    page.reg_btn_click()
    assert page.get_relative_link() != '/profile/orders/all/'


@pytest.mark.negative
@pytest.mark.parametrize('search_value', neg_search)
def test_search_neg(selenium, search_value):
    """Поиск товара негативный"""
    page = SearchAndMore(selenium, url)
    page.search_field_click()
    page.enter_search_value(search_value)
    page.search_btn_click()
    assert page.get_url_query() == f'digiSearch=true&term={search_value}'


@pytest.mark.positive
def test_login_correct(selenium):
    """Тест входа на сайт с правильными логином и паролем"""
    page = AuthPage(selenium, auth_url)
    page.enter_email(email)
    page.enter_pass(password)
    page.btn_click()
    assert page.get_relative_link() == '/profile/orders/all/'


@pytest.mark.positive
def test_registration(selenium):
    """Тест регистрации с валидной почтой. Почта генерируется рандомно"""
    page = AuthPage(selenium, auth_url)
    page.enter_registration_email(reg_email)
    page.reg_btn_click()
    assert page.get_relative_link() == '/profile/orders/all/'


@pytest.mark.positive
@pytest.mark.parametrize('sort_value', sorted_values)
def test_search_sort(selenium, sort_value):
    """Тест сорировки товаров"""
    page = SortedCheck(selenium, sorted_url, sort_value)
    assert page.get_sorted_result() == page.check_sorted_result(sort_value)


@pytest.mark.positive
def test_cart(selenium):
    """Тест добавления товара в корзину. Проверяется что цена товара на сайте ==
    цене в корзине"""
    page = Cart(selenium, url)
    ware_price = page.get_ware_price()
    page.put_ware_to_cart()
    price_at_cart = page.get_price_at_cart()
    assert ware_price == price_at_cart


@pytest.mark.positive
@pytest.mark.parametrize('search_value', search_values)
def test_search(selenium, search_value):
    """Тест поиска позиций на сайте по названию. Т.к. в результатах поиска может не быть точного вхождения названия,
    например из-за окончаний, то используется soft assert"""
    page = SearchAndMore(selenium, url)
    page.search_field_click()
    page.enter_search_value(search_value)
    page.search_btn_click()
    page.get_search_result()
    result = page.check_search()
    for ware in result:
        check.is_in(search_value, ware.lower())


@pytest.mark.positive
def test_filter_price(selenium):
    """Тест фильтра по цене в результатах поиска. Доступный ценовой диапазон делится на три части
    и цена подбирается рандомно"""
    page = FilterCheck(selenium, filter_check_url)
    new_min_price, new_max_price = page.enter_filter_price()
    result = page.get_wares_witch_filter()
    for ware_price in result:
        assert float(ware_price) >= new_min_price
        assert float(ware_price) <= new_max_price
