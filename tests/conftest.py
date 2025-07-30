import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import configparser
import os

from pages.login_page import LoginPage
from pages.products_page import ProductsPage


@pytest.fixture(scope="session")
def config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


@pytest.fixture(scope="function")
def driver(config):
    base_url = config['UI_SAUCEDEMO']['BASE_URL']

    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
    if os.path.exists(chromedriver_path):
        service = ChromeService(executable_path=chromedriver_path)
    else:
        try:
            service = ChromeService(ChromeDriverManager().install())
        except Exception as e:
            pytest.fail(
                f"Не вдалося встановити ChromeDriver за допомогою WebDriverManager: {e}. Переконайтесь, що chromedriver.exe знаходиться в корені проєкту або встановіть webdriver-manager.")

    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get(base_url)

    yield driver

    driver.quit()


# Фікстура для сторінки логіну
@pytest.fixture(scope="function")
def login_page(driver):
    """
    Фікстура, що надає об'єкт LoginPage для UI-тестів.
    """
    return LoginPage(driver)


# Фікстура для сторінки продуктів
@pytest.fixture(scope="function")
def products_page(driver):
    """
    Фікстура, що надає об'єкт ProductsPage для UI-тестів.
    """
    return ProductsPage(driver)
