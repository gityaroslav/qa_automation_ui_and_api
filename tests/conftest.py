import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import configparser
import os
import shutil
import tempfile
from pages.cart_page import CartPage
from pages.checkout_page_1 import CheckoutPageOne
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from selenium.webdriver.chrome.options import Options
import allure


@pytest.fixture(scope="session")
def config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


# Ця фікстура налаштовує і запускає браузер з розширеними параметрами
@pytest.fixture(scope="function")
def driver(config):
    base_url = config['UI_SAUCEDEMO']['BASE_URL']

    # Створюємо тимчасову папку для профілю, щоб тестувати в чистому середовищі
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

    # Використовуємо ChromeDriverManager для управління драйвером
    try:
        service = ChromeService(ChromeDriverManager().install())
    except Exception as e:
        pytest.fail(f"Не вдалося встановити ChromeDriver: {e}")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(base_url)

    yield driver

    driver.quit()
    # Видаляємо тимчасовий каталог після завершення тесту
    shutil.rmtree(temp_profile_dir, ignore_errors=True)


# Додаємо скриншот до звіту у випадку падіння тесту
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This function is a hook that runs after each test and gets its result
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Check if the test failed and has a driver fixture
        try:
            driver = item.funcargs['driver']
            # Take a screenshot
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Could not take a screenshot due to an error: {e}")


@pytest.fixture(scope="function")
def logged_in_standard_user(driver, config, login_page, products_page):
    login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
    login_page.login(config['UI_SAUCEDEMO']['USERNAME'], config['UI_SAUCEDEMO']['PASSWORD'])
    login_page.wait_for_url("https://www.saucedemo.com/inventory.html")
    return products_page


@pytest.fixture(scope="function")
def login_page(driver):
    """
    Фікстура, що надає об'єкт LoginPage для UI-тестів.
    """
    return LoginPage(driver)


@pytest.fixture(scope="function")
def products_page(driver):
    """
    Фікстура, що надає об'єкт ProductsPage для UI-тестів.
    """
    return ProductsPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver):
    """
    Фікстура, що надає об'єкт CartPage для UI-тестів.
    """
    return CartPage(driver)


@pytest.fixture(scope="function")
def checkout_page_1(driver):
    """
    Фікстура, що надає об'єкт CheckoutPage для UI-тестів.
    """
    return CheckoutPageOne(driver)