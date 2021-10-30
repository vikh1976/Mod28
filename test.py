import pytest
from pages import AuthPage, SearchAndMore, SortedCheck, Cart
import time

# Тесты: логин(негативные - цифры, символы, иероглиф, кириллица, 255 символов, пустое)
# пароль(негативные - цифры, символы, иероглиф, кириллица, 255 символов, пустое)
# регистрация (негативные - цифры, символы, иероглиф, кириллица, 255 символов, пустое)
# поиск (негативные - цифры, символы, иероглиф, кириллица, 100 символов, пустое)
# правильный логин и пароль, регистация с правильной почтой, выход
# сортировка - по возрастанию, убыванию, название.
# Добавление товара в корзину
import test_params


@pytest.mark.skip
@pytest.mark.parametrize('email', test_params.neg_email)
@pytest.mark.parametrize('password', test_params.neg_password)
def test_login_password_neg(selenium, email, password):
    page = AuthPage(selenium, test_params.auth_url)
    page.enter_email(email)
    page.enter_pass(password)
    page.btn_click()
    assert page.get_relative_link() != '/profile/orders/all/'


@pytest.mark.skip
@pytest.mark.parametrize('email', test_params.neg_email)
def test_register_neg(selenium, email):
    page = AuthPage(selenium, test_params.auth_url)
    page.enter_registration_email(email)
    page.reg_btn_click()
    assert page.get_relative_link() != '/profile/orders/all/'


@pytest.mark.skip
@pytest.mark.parametrize('search_value', test_params.neg_search)
def test_search_neg(selenium, search_value):
    page = SearchAndMore(selenium, test_params.url)
    page.search_field_click()
    page.enter_search_value(search_value)
    page.search_btn_click()
    assert page.get_url_query() == f'digiSearch=true&term={search_value}'


@pytest.mark.skip
def test_login_correct(selenium):
    page = AuthPage(selenium, test_params.auth_url)
    page.enter_email(test_params.email)
    page.enter_pass(test_params.password)
    page.btn_click()
    assert page.get_relative_link() == '/profile/orders/all/'


@pytest.mark.skip
def test_registration(selenium):
    page = AuthPage(selenium, test_params.auth_url)
    page.enter_registration_email(test_params.reg_email)
    page.reg_btn_click()
    assert page.get_relative_link() == '/profile/orders/all/'


@pytest.mark.skip
@pytest.mark.parametrize('sort_value', test_params.sorted_values)
def test_search_sort(selenium, sort_value):
    page = SortedCheck(selenium, test_params.sorted_url, sort_value)
    assert page.get_sorted_result() == page.check_sorted_result(sort_value)


@pytest.mark.skip
def test_cart(selenium):
    page = Cart(selenium, test_params.url)
    ware_price = page.get_ware_price()
    page.put_ware_to_cart()
    price_at_cart = page.get_price_at_cart()
    assert ware_price == price_at_cart




