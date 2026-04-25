# pages/common/base_page.py
import time
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

# -----------------------------------------------------------
# LOGGER
# -----------------------------------------------------------
from utilities.logger import logger

# ✅ NEW: config integration
from utilities.read_yaml import get_config

from selenium.common.exceptions import NoSuchElementException, TimeoutException


class BasePage:
    def __init__(self, driver, timeout=None):   # ✅ UPDATED
        self.driver = driver
        # ✅ take from config if not passed
        self.timeout = timeout if timeout else get_config("explicit_wait", 10)

    # -------------------------------------------------------------------
    # 📸 Take Screenshot
    # -------------------------------------------------------------------
    def _screenshot(self, name="failure"):
        folder = "reports/screenshots"
        os.makedirs(folder, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        file = f"{folder}/{name}_{ts}.png"

        try:
            self.driver.save_screenshot(file)
            logger.info(f"📸 Screenshot saved: {file}")
        except Exception as e:
            logger.error(f"Failed saving screenshot: {e}")

    def is_element_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, StaleElementReferenceException):
            return False

    # -------------------------------------------------------------------
    # 🔥 WAIT helper
    # -------------------------------------------------------------------
    def wait(self, locator, condition=EC.visibility_of_element_located, timeout=None):
        t = timeout if timeout is not None else self.timeout
        try:
            logger.info(f"Waiting for: {locator}")
            return WebDriverWait(self.driver, t).until(condition(locator))
        except Exception as e:
            logger.error(f"[WAIT FAILED] {locator} → {e}")
            self._screenshot("wait_failed")
            raise

    # -------------------------------------------------------------------
    # 🔥 CLICK (ENHANCED)
    # -------------------------------------------------------------------
    def click(self, locator):
        attempts = 3

        for attempt in range(attempts):
            try:
                logger.info(f"Clicking: {locator}")

                # ✅ UPDATED: wait for clickable instead of presence
                # element = self.wait(locator, EC.element_to_be_clickable)
                element = self.wait(locator, EC.presence_of_element_located)
                # Scroll into center
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", element
                    )
                except:
                    pass

                time.sleep(0.1)

                try:
                    element.click()
                except:
                    # JS fallback
                    self.driver.execute_script("arguments[0].click();", element)

                time.sleep(0.2)
                logger.info(f"Clicked successfully: {locator}")
                return

            except Exception as e:
                logger.warning(f"[CLICK FAILED] Attempt {attempt+1}/3 for {locator} → {e}")

                if attempt == attempts - 1:
                    self._screenshot("click_failed")
                    logger.error(f"Click ultimately failed: {locator}")
                    raise

                time.sleep(0.5)

    # -------------------------------------------------------------------
    # 🔥 TYPE (ENHANCED)
    # -------------------------------------------------------------------
    def type(self, locator, text, timeout=None):   # ✅ UPDATED
        t = timeout if timeout else self.timeout

        element = WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator)   # ✅ UPDATED
        )

        try:
            element.clear()
            element.send_keys(text)
        except Exception:
            # React fallback
            self.driver.execute_script(
                """
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                """,
                element,
                text
            )

    # -------------------------------------------------------------------
    # 🔥 GET TEXT
    # -------------------------------------------------------------------
    def get_text(self, locator):
        try:
            el = self.wait(locator)
            text = el.text
            logger.info(f"Got text from {locator}: {text}")
            return text
        except Exception as e:
            logger.error(f"[GET TEXT FAILED] {locator} → {e}")
            self._screenshot("gettext_failed")
            raise

    # -------------------------------------------------------------------
    def is_visible(self, locator):
        try:
            return self.wait(locator)
        except:
            return False

    # -------------------------------------------------------------------
    def open(self, url):
        try:
            logger.info(f"Opening URL: {url}")
            self.driver.get(url)
            time.sleep(1)
        except Exception as e:
            logger.error(f"[OPEN FAILED] {url} → {e}")
            self._screenshot("open_failed")
            raise

    # -------------------------------------------------------------------
    def is_present(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def get_value(self, locator):
        element = self.wait(locator)
        return element.get_attribute("value")

    def clear(self, locator):
        element = self.wait(locator, EC.element_to_be_clickable)  # ✅ UPDATED
        element.clear()

    def select_by_visible_text(self, locator, text):
        element = self.driver.find_element(*locator)
        select = Select(element)
        select.select_by_visible_text(text)

    def wait_until_enabled(self, locator, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*locator).is_enabled()
        )

    def make_editable(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script(
            "arguments[0].removeAttribute('readonly')", element
        )

    def has_any_validation_error(self):
        return (
                len(self.driver.find_elements(By.CLASS_NAME, "invalid-feedback")) > 0
                or len(self.driver.find_elements(By.XPATH, "//div[contains(@class,'toast-body')]")) > 0
        )

    def send_keys(self, locator, value):
        self.driver.find_element(*locator).send_keys(value)

    def get_element(self, locator):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )

    def enter_text(self, locator, text):
        element = self.get_element(locator)
        element.clear()
        element.send_keys(text)

    def select_searchable_dropdown(self, locator, value):
        self.click(locator)

        search = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(@class,'choices') and contains(@class,'is-open')]//input"
            ))
        )

        search.clear()
        search.send_keys(value)

        # ✅ WAIT UNTIL OPTION APPEARS (REAL FIX)
        option = WebDriverWait(self.driver, 15).until(
            lambda d: next(
                (
                    el for el in d.find_elements(
                    By.XPATH,
                    "//div[contains(@class,'choices__list--dropdown')]//div[@role='option']"
                )
                    if value.lower() in el.text.lower()
                ),
                None
            )
        )

        if not option:
            raise Exception(f"{value} not found in dropdown")

        self.driver.execute_script("arguments[0].scrollIntoView(true);", option)
        option.click()

    def select_status_keyboard(self, locator, value):
        self.click(locator)
        time.sleep(1)

        active_element = self.driver.switch_to.active_element

        if value.lower() == "active":
            active_element.send_keys(Keys.ARROW_DOWN)
        elif value.lower() == "inactive":
            active_element.send_keys(Keys.ARROW_DOWN)
            active_element.send_keys(Keys.ARROW_DOWN)

        active_element.send_keys(Keys.ENTER)

    # 🔥 ADD THIS IN BasePage

    def select_dropdown(self, locator, text):

        # click dropdown
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        dropdown.click()

        # wait for options (VERY IMPORTANT)
        options = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((
                By.XPATH, "//div[@role='option']"
            ))
        )

        print("OPTIONS FOUND:", [o.text for o in options])

        # click matching option
        for option in options:
            if text.strip() in option.text.strip():
                option.click()
                return

        raise Exception(f"❌ Option '{text}' not found")