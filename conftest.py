import os
import pytest
from datetime import datetime

import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.support.ui import WebDriverWait

from utilities.read_yaml import read_config


# =========================================================
# Load config.yaml only once
# =========================================================
config = read_config()


# =========================================================
# CLI option → browser selection
# =========================================================
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser: chrome, edge, firefox, ulaa"
    )


# =========================================================
# Fixtures
# =========================================================
@pytest.fixture(scope="session")
def get_browser(request):
    return request.config.getoption("--browser").lower()


@pytest.fixture(scope="session")
def get_config():
    return config


@pytest.fixture(scope="session")
def base_url(get_config):
    return get_config["url"]


@pytest.fixture()
def wait(setup, get_config):
    timeout = get_config.get("explicit_wait", 10)
    return WebDriverWait(setup, timeout)


# =========================================================
# CLEAN OLD ARTIFACTS (Screenshots)
# =========================================================
@pytest.fixture(scope="session", autouse=True)
def clean_old_reports():
    screenshots_dir = "reports/screenshots"

    if os.path.exists(screenshots_dir):
        shutil.rmtree(screenshots_dir)

    os.makedirs(screenshots_dir, exist_ok=True)

# =========================================================
# MAIN DRIVER SETUP (Chrome / Edge / Firefox / Ulaa)
# =========================================================
@pytest.fixture()
def setup(request, get_browser, get_config, base_url):

    browser = get_browser
    is_ci = os.getenv("CI", "false").lower() == "true"

    # --------------------------------------
    # Browser → Chrome
    # --------------------------------------
    if browser == "chrome":
        options = ChromeOptions()

        if get_config.get("headless", False) or is_ci:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)

    # --------------------------------------
    # Browser → Edge
    # --------------------------------------
    elif browser == "edge":
        options = EdgeOptions()
        if get_config.get("headless", False) or is_ci:
            options.add_argument("headless")
            options.add_argument("window-size=1920,1080")
        driver = webdriver.Edge(options=options)

    # --------------------------------------
    # Browser → Firefox
    # --------------------------------------
    elif browser == "firefox":
        options = FirefoxOptions()
        if get_config.get("headless", False) or is_ci:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    # --------------------------------------
    # Browser → ULAA
    # --------------------------------------
    elif browser == "ulaa":
        options = ChromeOptions()
        ulaa_path = get_config.get("ulaa_path", "")
        if not os.path.exists(ulaa_path):
            raise FileNotFoundError(
                f"ULAA browser not found at: {ulaa_path}"
            )
        options.binary_location = ulaa_path

        if get_config.get("headless", False) or is_ci:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)

    else:
        raise ValueError("Invalid browser. Use: chrome / edge / firefox / ulaa")

    # --------------------------------------
    # Browser common settings
    # --------------------------------------
    driver.maximize_window()
    driver.implicitly_wait(get_config.get("implicit_wait", 10))

    # --------------------------------------
    # Navigate to base URL
    # --------------------------------------
    driver.get(base_url)

    # ---------------------------------------------------------
    # ACCESS CODE AUTO-HANDLER (Correct position)
    # ---------------------------------------------------------
    if "accessCheck" in driver.current_url:
        from pages.common.access_code_page import AccessCodePage

        access_code = get_config.get("access_code")
        assert access_code, "Access code missing in config.yaml"

        access_page = AccessCodePage(driver)
        access_page.enter_and_submit(access_code)

    # Attach driver to test classes
    request.cls.driver = driver

    yield driver
    driver.quit()


# =========================================================
# LOGIN FIXTURE → Super Admin
# =========================================================
@pytest.fixture()
def login_superadmin(setup, get_config):
    from pages.superadmin.Login.sa_login_page import SuperAdminLoginPage

    user = get_config["users"]["superadmin"]
    SuperAdminLoginPage(setup).login(user["username"], user["password"])
    return setup


# =========================================================
# LOGIN FIXTURE → Manufacturer
# =========================================================
@pytest.fixture()
def login_manufacturer(setup, get_config):
    from pages.manufacturer.mf_login_page import ManufacturerLogin

    user = get_config["users"]["manufacturer"]
    ManufacturerLogin(setup).login(user["username"], user["password"])
    return setup


# =========================================================
# AUTOMATIC SCREENSHOT ON FAILURE
# =========================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("setup")

        if driver:
            # ALWAYS resolve path from project root
            project_root = os.getcwd()
            folder = os.path.join(project_root, "reports", "screenshots")
            os.makedirs(folder, exist_ok=True)

            file_name = (
                f"{report.nodeid.replace('::','_')}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )

            filepath = os.path.join(folder, file_name)
            driver.save_screenshot(filepath)

            print(f"\n Screenshot saved: {filepath}")

            # Optional: Allure
            try:
                import allure
                with open(filepath, "rb") as f:
                    allure.attach(
                        f.read(),
                        name="Failure Screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
            except:
                pass
