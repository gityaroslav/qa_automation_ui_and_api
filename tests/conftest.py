import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import configparser
import os
import shutil
import tempfile
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


@pytest.fixture(scope="function")
def driver(config):
    base_url = config['UI_SAUCEDEMO']['BASE_URL']

    # Тимчасовий чистий профіль
    temp_profile_dir = tempfile.mkdtemp()

    chrome_options = Options()

    # Головне: режим інкогніто + відключення перевірок
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument(f"--user-data-dir={temp_profile_dir}")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--start-maximized")

    # Відключення features, які відповідають за перевірку паролів
    chrome_options.add_argument(
        "--disable-features=PasswordCheck,AutofillServerCommunication,PasswordManagerOnboarding,OptimizationGuideModelDownloading,Translate")

    # Повна заборона менеджера паролів
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2
    })

    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
    if os.path.exists(chromedriver_path):
        service = ChromeService(executable_path=chromedriver_path)
    else:
        try:
            service = ChromeService(ChromeDriverManager().install())
        except Exception as e:
            pytest.fail(f"Не вдалося встановити ChromeDriver: {e}")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(base_url)

    yield driver

    driver.quit()
    shutil.rmtree(temp_profile_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def logged_in_standard_user(driver, config, login_page, products_page):
    login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
    login_page.login(config['UI_SAUCEDEMO']['USERNAME'], config['UI_SAUCEDEMO']['PASSWORD'])
    login_page.wait_for_url("https://www.saucedemo.com/inventory.html")
    return products_page


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


@pytest.fixture(scope="function")
def cart_page(driver):  # <-- NEW FIXTURE
    """
    Фікстура, що надає об'єкт CartPage для UI-тестів.
    """
    return CartPage(driver)
