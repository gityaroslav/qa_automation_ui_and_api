from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select


class BasePage:
    SHOPPING_CART_ICON = (By.ID, "shopping_cart_container")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    BURGER_MENU_ICON = (By.ID, "react-burger-menu-btn")
    BURGER_LOGOUT = (By.ID, "logout_sidebar_link")
    BURGER_MENU_WRAPPER = (By.CLASS_NAME, "bm-menu-wrap")
    BURGER_MENU_RESET = (By.ID, "reset_sidebar_link")
    BURGER_MENU_CLOSE = (By.ID, "react-burger-cross-btn")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click_element(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, element_or_locator) -> str:
        if isinstance(element_or_locator, WebElement):
            return element_or_locator.text
        elif isinstance(element_or_locator, tuple) and len(element_or_locator) == 2:
            element = self.find_element(element_or_locator)
            return element.text

    def is_element_displayed(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False

    def wait_for_url(self, expected_url):
        self.wait.until(EC.url_to_be(expected_url))

    def get_current_url(self):
        return self.driver.current_url

    def click_shopping_cart_icon(self):
        from pages.cart_page import CartPage
        self.click_element(self.SHOPPING_CART_ICON)
        return CartPage(self.driver)

    def get_shopping_cart_badge_count(self):
        try:
            badge_element = self.find_element(self.SHOPPING_CART_BADGE)
            return int(badge_element.text)
        except:
            return 0

    def select_by_value(self, locator, value):
        select_element = self.find_element(locator)
        select = Select(select_element)
        select.select_by_value(value)

    def click_burger_menu(self):
        self.click_element(self.BURGER_MENU_ICON)
        self.wait_for_element_is_displayed(self.BURGER_MENU_WRAPPER)

    def click_burger_logout(self):
        from pages.login_page import LoginPage
        self.click_element(self.BURGER_LOGOUT)
        return LoginPage(self.driver)

    def click_burger_menu_reset(self):
        self.click_element(self.BURGER_MENU_RESET)
        self.click_element(self.BURGER_MENU_CLOSE)

    def wait_for_element_is_displayed(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
