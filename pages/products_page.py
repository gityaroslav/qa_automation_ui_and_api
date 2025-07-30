from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductsPage(BasePage):
    PRODUCTS_TITLE = (By.XPATH, "//span[@class='title' and text()='Products']")
    ALL_PRODUCT_IMAGES = (By.XPATH, "//img[@class='inventory_item_img']")

    def __init__(self, driver):
        super().__init__(driver)

    def is_products_page_displayed(self):
        return self.is_element_displayed(self.PRODUCTS_TITLE)

    def get_products_title_text(self):
        return self.get_element_text(self.PRODUCTS_TITLE)

