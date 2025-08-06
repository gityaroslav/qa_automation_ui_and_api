from selenium.webdriver.common.by import By
import random
from pages.base_page import BasePage
from pages.checkout_page_1 import CheckoutPageOne


class CartPage(BasePage):

    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CART_TITLE = (By.XPATH, "//span[@class='title' and text()='Your Cart']")
    CART_ITEM_NAME_BY_TEXT = lambda self, item_name: (
        By.XPATH, f"//div[@class='inventory_item_name' and text()='{item_name}']")
    REMOVE_CART_BUTTONS = (By.XPATH, "//button[contains(@class, 'btn_secondary') and contains (text(), 'Remove')]")
    ADDED_PRODUCTS = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_NAME_FROM_ADDED_PRODUCTS = (By.XPATH, "./ancestor::div[@class='cart_item_label']//div["
                                                  "@class='inventory_item_name']")

    def __init__(self, driver):
        super().__init__(driver)

    def is_cart_page_displayed(self):
        return self.is_element_displayed(self.CART_TITLE)

    def is_item_in_cart_by_name(self, item_name):
        locator = self.CART_ITEM_NAME_BY_TEXT(item_name)
        return self.is_element_displayed(locator)

    def remove_random_item_from_cart(self):
        all_remove_buttons = self.find_elements(self.REMOVE_CART_BUTTONS)
        random_remove_button = random.choice(all_remove_buttons)
        removed_product = random_remove_button.find_element(*self.PRODUCT_NAME_FROM_ADDED_PRODUCTS)
        removed_product_name = removed_product.text
        random_remove_button.click()
        return removed_product_name

    def get_cart_items_names(self):
        added_products_names = []
        added_products_list = self.find_elements(self.ADDED_PRODUCTS)
        for product in added_products_list:
            name = self.get_element_text(product)
            added_products_names.append(name)
        return added_products_names

    def click_checkout_button(self):
        self.click_element(self.CHECKOUT_BUTTON)
        assert self.get_current_url() == "https://www.saucedemo.com/checkout-step-one.html"
        return CheckoutPageOne(self.driver)

