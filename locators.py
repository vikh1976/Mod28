from selenium.webdriver.common.by import By


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


class SortedCheckLocators:
    LOAD_MORE = (By.XPATH, '//div[@id="catalog_loadmore"]/a')
    WARES_CLASS = 'btn btn-primary add-to-cart'
    NAME_ID = 'data-title'
    PRICE_ID = 'data-price'



