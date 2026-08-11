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
from utilities.read_yaml import read_config, get_config_value
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
        default=None,
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
        browser = get_config_value("browser")

    print("=" * 60)
    print("Browser Selected :", browser)
    print("=" * 60)

    return browser.lower()


@pytest.fixture(scope="session")
def get_config():
    return config

@pytest.fixture(scope="session")
def get_login_user(get_config):

    worker = os.getenv("PYTEST_XDIST_WORKER", "master")

    worker_map = {
        "master": 0,
        "gw0": 0,
        "gw1": 1,
        "gw2": 2,
        "gw3": 3,
        "gw4": 4,
        "gw5": 5,
    }

    index = worker_map.get(worker, 0)

    users = get_config["automation_users"]

    if index >= len(users):
        raise Exception(
            f"No automation account configured for {worker}"
        )

    user = users[index]

    print("=" * 60)
    print("Worker :", worker)
    print("Username :", user["username"])
    print("=" * 60)

    return user


@pytest.fixture(scope="session")
def base_url(get_config):

    # 1. Jenkins parameter
    env = os.getenv("ENVIRONMENT")

    # 2. config.yaml
    if not env:
        env = get_config_value("environment")

    print("=" * 60)
    print("Environment :", env)
    print("=" * 60)

    return get_config["urls"][env]

def get_headless():
    headless = os.getenv("HEADLESS")

    if headless is None:
        return get_config_value("execution.headless")

    return headless.lower() == "true"

@pytest.fixture()
def wait(setup, get_config):
    timeout = get_config["timeouts"]["explicit_wait"]
    return WebDriverWait(setup, timeout)


# =========================================================
# CLEAN OLD ARTIFACTS (Screenshots)
# =========================================================
@pytest.fixture(scope="session", autouse=True)
def clean_old_reports(request):

    # Only run in the master process
    if hasattr(request.config, "workerinput"):
        return

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
def setup(request, get_browser, get_config, base_url):

    browser = get_browser
    is_ci = os.getenv("CI", "false").lower() == "true"
    # DEBUG
    print("=" * 60)
    print("CI Environment :", os.getenv("CI"))
    print("is_ci          :", is_ci)
    print("Headless :", get_headless())
    print("=" * 60)

    # --------------------------------------
    # Browser → Chrome
    # --------------------------------------
    if browser == "chrome":
        options = ChromeOptions()

        if get_headless():
            print("Running in Headless Mode")
            options.add_argument("--headless=new")
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
        worker = os.getenv("PYTEST_XDIST_WORKER", "master")

        download_path = os.path.join(
            os.getcwd(),
            "downloads",
            worker
        )

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

        if get_headless():
            options.add_argument("--headless")
        else:
            print("Running Firefox in Headed Mode")

        driver = webdriver.Firefox(options=options)

    elif browser == "edge":
        options = EdgeOptions()

        if get_headless():
            options.add_argument("--headless=new")
        else:
            print("Running Edge in Headed Mode")

        driver = webdriver.Edge(options=options)
    # --------------------------------------
    # --------------------------------------
    # Browser → ULAA
    # --------------------------------------
    elif browser == "ulaa":

        print("=" * 60)
        print("Launching ULAA Browser")
        print("=" * 60)

        options = ChromeOptions()

        ulaa_path = get_config["ulaa"]["path"]

        if not os.path.exists(ulaa_path):
            raise FileNotFoundError(
                f"ULAA browser not found at: {ulaa_path}"
            )

        options.binary_location = ulaa_path

        # Force a desktop-size viewport
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--force-device-scale-factor=1")

        # Same compatibility options
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-allow-origins=*")
        options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )

        if get_headless():
            print("Running ULAA in Headless Mode")
            options.add_argument("--headless=new")
        else:
            print("Running ULAA in Headed Mode")

        driver = webdriver.Chrome(options=options)

        # Explicitly force window size after driver creation
        try:
            driver.set_window_size(1920, 1080)

            print("ULAA Window Size:",
                  driver.get_window_size())

            print("ULAA Viewport:",
                  driver.execute_script("""
                      return {
                          width: window.innerWidth,
                          height: window.innerHeight
                      };
                  """))

        except Exception as e:
            print("Could not set ULAA window size:", e)

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
        get_config["timeouts"]["implicit_wait"]
    )
    driver.set_page_load_timeout(
        get_config["timeouts"]["page_load_timeout"]
    )

    # --------------------------------------
    # Navigate to base URL
    # --------------------------------------
    print("=" * 60)
    print("FINAL BROWSER SIZE :", driver.get_window_size())
    print("FINAL VIEWPORT     :", driver.execute_script("""
        return {
            width: window.innerWidth,
            height: window.innerHeight
        };
    """))
    print("=" * 60)

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
            worker = os.getenv("PYTEST_XDIST_WORKER", "master")

            folder = os.path.join(
                project_root,
                "reports",
                "screenshots",
                worker
            )

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
def login_superadmin(setup, get_login_user):

    login_page = SuperAdminLoginPage(setup)

    username = login_page.login_successfully(
        get_login_user["username"],
        get_login_user["password"]
    )

    return {
        "driver": setup,
        "username": username
    }