import os
import pytest
from datetime import datetime

import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.support.ui import WebDriverWait
from pages.superadmin.Login.sa_login_page import SuperAdminLoginPage
from utilities.read_yaml import read_config, get_config
import pytest
from utilities.data_generator import generate_category_name
from selenium.webdriver.support import expected_conditions as EC
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
        default="None",
        help="Browser: chrome, edge, firefox, ulaa"
    )


# =========================================================
# Fixtures
# =========================================================
@pytest.fixture(scope="session")
def get_browser(request):

    # 1. Jenkins Parameter
    browser = os.getenv("BROWSER")

    # 2. Pytest CLI
    if not browser:
        browser = request.config.getoption("--browser")

    # 3. config.yaml
    # 3. config.yaml
    if not browser:
        browser = get_config("browser")

    print("=" * 60)
    print("Browser Selected :", browser)
    print("=" * 60)

    return browser.lower()


@pytest.fixture(scope="session")
def config_data():
    return config


@pytest.fixture(scope="session")
def base_url(config_data):

    env = config_data["environment"]

    return config_data["urls"][env]


@pytest.fixture()
def wait(setup, config_data):
    timeout = config_data["timeouts"]["explicit_wait"]
    return WebDriverWait(setup, timeout)


# =========================================================
# CLEAN OLD ARTIFACTS (Screenshots)
# =========================================================
@pytest.fixture(scope="session", autouse=True)
def clean_old_reports():

    folders = [
        "reports/screenshots",
        "reports/html"
    ]

    for folder in folders:

        if os.path.exists(folder):
            shutil.rmtree(folder)

        os.makedirs(folder, exist_ok=True)

# =========================================================
# MAIN DRIVER SETUP (Chrome / Edge / Firefox / Ulaa)
# =========================================================
@pytest.fixture()
def setup(request, get_browser, config_data, base_url):

    browser = get_browser
    is_ci = os.getenv("CI", "false").lower() == "true"
    # DEBUG
    print("=" * 60)
    print("CI Environment :", os.getenv("CI"))
    print("is_ci          :", is_ci)
    print("Headless :", get_config("execution.headless"))
    print("=" * 60)

    # --------------------------------------
    # Browser → Chrome
    # --------------------------------------
    if browser == "chrome":
        options = ChromeOptions()

        if is_ci or get_config("execution.headless"):
            print("Running in Headless Mode")
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        else:
            print("Running in Headed Mode")

        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Chrome 150 compatibility
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # --------------------------------------
        # Download Folder
        # --------------------------------------
        download_path = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_path, exist_ok=True)

        prefs = {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }

        options.add_experimental_option("prefs", prefs)


        driver = webdriver.Chrome(options=options)

    # --------------------------------------
    # Browser → Firefox
    # --------------------------------------
    elif browser == "firefox":
        options = FirefoxOptions()
        if is_ci or config_data["execution"]["headless"]:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    elif browser == "edge":
        options = EdgeOptions()

        if is_ci or get_config("execution.headless"):
            print("Running Edge in Headless Mode")
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        else:
            print("Running Edge in Headed Mode")

        driver = webdriver.Edge(options=options)
    # --------------------------------------
    # Browser → ULAA
    # --------------------------------------
    elif browser == "ulaa":
        options = ChromeOptions()
        ulaa_path = config_data["ulaa"]["path"]
        if not os.path.exists(ulaa_path):
            raise FileNotFoundError(
                f"ULAA browser not found at: {ulaa_path}"
            )
        options.binary_location = ulaa_path

        if is_ci or get_config("execution.headless"):
            print("Running ULAA in Headless Mode")
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        else:
            print("Running ULAA in Headed Mode")

        driver = webdriver.Chrome(options=options)

    else:
        raise ValueError("Invalid browser. Use: chrome / edge / firefox / ulaa")

    # --------------------------------------
    # Browser common settings
    # --------------------------------------
    try:
        driver.maximize_window()
        print(driver.get_window_size())
        driver.set_window_size(1920, 1080)
        print("After set:", driver.get_window_size())
    except Exception:
        pass
    driver.implicitly_wait(
        config_data["timeouts"]["implicit_wait"]
    )
    driver.set_page_load_timeout(
        config_data["timeouts"]["page_load_timeout"]
    )

    # --------------------------------------
    # Navigate to base URL
    # --------------------------------------
    driver.get(base_url)

    # ---------------------------------------------------------
    # ACCESS CODE AUTO-HANDLER (Correct position)
    # ---------------------------------------------------------
    if "accessCheck" in driver.current_url:
        from pages.common.access_code_page import AccessCodePage

        access_code = config_data.get("access_code")
        assert access_code, "Access code missing in config.yaml"

        access_page = AccessCodePage(driver)
        access_page.enter_and_submit(access_code)
        print("Current URL after submit:", driver.current_url)
        print("Page Title:", driver.title)
        WebDriverWait(driver, 20).until(
            lambda d: "accessCheck" not in d.current_url
        )
        print(driver.execute_script("""
        return document.querySelector("input[name='email']").value;
        """))

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "email"))
        )

        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script(
                "return document.readyState==='complete'"
            )
        )

        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script(
                "return document.querySelector(\"button[type='submit']\").offsetParent!==null"
            )
        )

        print("Email before typing:",
              driver.execute_script(
                  "return document.querySelector(\"input[name='email']\").value;"
              ))

    # Attach driver to test classes
    request.cls.driver = driver

    yield driver
    driver.quit()


# =========================================================
# LOGIN FIXTURE → Super Admin
# =========================================================


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

            safe_name = (
                report.nodeid
                .replace("::", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            file_name = (
                f"{safe_name}_"
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



@pytest.fixture
def category_name():
    return generate_category_name()

@pytest.fixture()
def login_superadmin(setup, config_data):
    user = config_data["users"]["superadmin"]

    login_page = SuperAdminLoginPage(setup)

    username = login_page.login_successfully(
        user["username"],
        user["password"]
    )

    return {
        "driver": setup,
        "username": username
    }