import pytest
from selenium import webdriver
from utilities.read_yaml import read_config
from selenium.webdriver.chrome.options import Options

config = read_config()

@pytest.fixture(scope="session")
def get_config():
    return config

@pytest.fixture()
def setup(get_config):
    opts = Options()
    if get_config.get("headless", False):
        opts.add_argument("--headless")
        opts.add_argument("--window-size=1920,1080")
    # disable GPU on some Windows CI
    opts.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=opts)
    driver.maximize_window()
    driver.implicitly_wait(get_config.get("implicit_wait", 10))
    driver.get(get_config["url"])
    yield driver
    driver.quit()

@pytest.fixture()
def login_superadmin(setup, get_config):
    from pages.superadmin.sa_login_page import SuperAdminLogin
    user = get_config["users"]["superadmin"]
    SuperAdminLogin(setup).login(user["username"], user["password"])
    return setup

@pytest.fixture()
def login_manufacturer(setup, get_config):
    from pages.manufacturer.mf_login_page import ManufacturerLogin
    user = get_config["users"]["manufacturer"]
    ManufacturerLogin(setup).login(user["username"], user["password"])
    return setup
