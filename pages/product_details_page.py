from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.products_page import ProductsPage


class ProductDetailsPage(BasePage):
    PRODUCT_NAME = (By.XPATH, "//div[contains(@class, 'inventory_details_name')]")
    PRODUCT_DESCRIPTION = (By.XPATH, "//div[contains(@class, 'inventory_details_desc ')]")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_details_price")
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart")
    BACK_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver):
        super().__init__(driver)

    def get_product_name(self):
        return self.get_element_text(self.PRODUCT_NAME)

    def get_product_price(self):
        return self.get_element_text(self.PRODUCT_PRICE)

    def get_product_description(self):
        return self.get_element_text(self.PRODUCT_DESCRIPTION)

    def get_all_product_details(self):
        return {
            "name": self.get_product_name(),
            "description": self.get_product_description(),
            "price": self.get_product_price()
        }

    def click_back_to_products_button(self):
        self.click_element(self.BACK_BUTTON)
        return ProductsPage(self.driver)