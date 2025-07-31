from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):

    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CART_TITLE = (By.XPATH, "//span[@class='title' and text()='Your Cart']")
    CART_ITEM_NAME_BY_TEXT = lambda self, item_name: (
        By.XPATH, f"//div[@class='inventory_item_name' and text()='{item_name}']")


    def __init__(self, driver):
        super().__init__(driver)

    def is_cart_page_displayed(self):
        return self.is_element_displayed(self.CART_TITLE)

    def is_item_in_cart_by_name(self, item_name):
        """Перевіряє, чи відображається товар з заданою назвою у кошику."""
        locator = self.CART_ITEM_NAME_BY_TEXT(item_name)
        return self.is_element_displayed(locator)