import random
import re
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductsPage(BasePage):
    PRODUCTS_TITLE = (By.XPATH, "//span[@class='title' and text()='Products']")
    ALL_PRODUCT_IMAGES = (By.XPATH, "//img[@class='inventory_item_img']")
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    ALL_PRODUCT_LIST = (By.XPATH, "//button[contains(@class, 'btn_inventory') and contains(text(), 'Add to cart')]")
    PRODUCT_NAME_FROM_LIST = (By.XPATH, """
            ./ancestor::div[contains(@class,'inventory_item_description')]
            //div[contains(@class,'inventory_item_name')]
        """)
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    PRODUCTS_PRICES = (By.XPATH, "//div[@class='inventory_item_price']")

    def __init__(self, driver):
        super().__init__(driver)

    def is_products_page_displayed(self):
        return self.is_element_displayed(self.PRODUCTS_TITLE)

    def get_products_title_text(self):
        return self.get_element_text(self.PRODUCTS_TITLE)

    def get_shopping_cart_badge_count(self):
        return self.get_element_text(self.SHOPPING_CART_BADGE)

    def add_sauce_labs_backpack_to_cart(self):
        self.click_element(self.ADD_BACKPACK)

    def is_add_backpack_button_displayed(self):
        return self.is_element_displayed(self.ADD_BACKPACK)

    def is_remove_backpack_button_displayed(self):
        return self.is_element_displayed(self.REMOVE_BACKPACK)

    def add_random_products_to_cart(self):
        product_list = self.find_elements(self.ALL_PRODUCT_LIST)
        count = random.randint(1, len(product_list))
        random_products = random.sample(product_list, count)
        for product in random_products:
            product.click()
        return count

    def add_random_products_to_cart_and_get_names(self):
        product_list = self.find_elements(self.ALL_PRODUCT_LIST)
        count = random.randint(2, len(product_list))
        random_products = random.sample(product_list, count)
        added_products_texts = []
        for product in random_products:
            product_name_element = product.find_element(*self.PRODUCT_NAME_FROM_LIST)
            product_name_element_text = product_name_element.text
            added_products_texts.append(product_name_element_text)
            product.click()
        return added_products_texts

    def select_sorting_products_by_value(self, value):
        self.select_by_value(self.SORT_SELECT, value)

    def get_products_prices(self):
        products_list = self.find_elements(self.PRODUCTS_PRICES)
        product_prices = []
        for product in products_list:
            text = product.text
            price = float(re.findall(r'\d+\.\d+', text)[0])
            product_prices.append(price)
        return product_prices

