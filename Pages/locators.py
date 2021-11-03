from selenium.webdriver.common.by import By

# Классы для локаторов элементов страниц


class AuthLocators:
    AUTH_EMAIL = (By.XPATH, "//div[@class='form-group mt-20']/input")
    AUTH_PASS = (By.XPATH, "//div[@class='form-group']/input")
    AUTH_BTN = (By.XPATH, "//a[@class='btn btn-block btn-primary text-uppercase font-weight-bold auth_button']")
    REG_EMAIL = (By.XPATH, '//input[@id="reg_email"]')
    REG_BTN = (By.XPATH, "//a[@class='btn btn-block btn-primary text-uppercase font-weight-bold reg_button']")


class SearchLocators:
    SEARCH_FIELD_CLICK = (By.XPATH, "//input[@class='form-control suggest_search digi-instant-search jc-ignore']")
    SEARCH_FIELD = (By.XPATH, "//input[@class='digi-search-form__input']")
    SEARCH_BTN = (By.XPATH, "//button[@class='digi-search-form__submit']")
    SCROLL_UP = (By.XPATH, '//button[@class="digi-scroll-up"]')
    WARE = 'digi-product__label'


class SortedCheckLocators:
    LOAD_MORE = (By.XPATH, '//div[@id="catalog_loadmore"]/a')
    WARES_CLASS = 'btn btn-primary add-to-cart'
    NAME_ID = 'data-title'
    PRICE_ID = 'data-price'


class CartLocators:
    WARE = (By.XPATH, '//div[@class="col-6 col-sm-6 col-xl-4 mt-4 key_0"]')
    BUY_BTN =(By.XPATH, '//div[@class="buy_buttons buy_buttons_ buy_buttons__   selected"]')
    PRICE = (By.XPATH, '//span[@id="price"]')
    PRICE_CART = (By.XPATH, '//div[@class="signprice signprice-small text-nowrap mt-1 text-right"]')


class FilterLocators:
    MIN_PRICE = (By.XPATH, '//input[@name="min"]')
    MAX_PRICE = (By.XPATH, '//input[@name="max"]')
    PAGE_CLICK = By.XPATH, '//div[@class="digi-products"]'
    WARE_CLASS = 'digi-product-price-variant digi-product-price-variant_actual'




