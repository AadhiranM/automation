from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def click(self, locator):
        WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).clear()
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def get_text(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))

    def open(self, url):
        self.driver.get(url)
