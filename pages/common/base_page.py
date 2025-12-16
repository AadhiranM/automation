# pages/common/base_page.py
import time
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# -----------------------------------------------------------
# ALWAYS use the global logger (NO fallback logger here)
# -----------------------------------------------------------
from utilities.logger import logger

from selenium.common.exceptions import NoSuchElementException, TimeoutException


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    # -------------------------------------------------------------------
    # 📸 Take Screenshot (used internally on failure)
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
        """
        Returns True if element becomes visible within timeout.
        Returns False if not found / not visible.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, StaleElementReferenceException):
            return False

    # -------------------------------------------------------------------
    # 🔥 WAIT helper (all waits use this)
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
    # 🔥 CLICK (scroll → normal click → JS click → retry)
    # -------------------------------------------------------------------
    def click(self, locator):
        attempts = 3

        for attempt in range(attempts):
            try:
                logger.info(f"Clicking: {locator}")
                element = self.wait(locator, EC.presence_of_element_located)

                # Scroll into center
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", element
                    )
                except:
                    pass
                time.sleep(0.1)

                # Normal click
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
    # 🔥 TYPE (clear + send keys safely)
    # -------------------------------------------------------------------
    def type(self, locator, text):
        try:
            logger.info(f"Typing into {locator}: '{text}'")
            element = self.wait(locator, EC.visibility_of_element_located)
            element.clear()
            time.sleep(0.05)
            element.send_keys(text)
            time.sleep(0.15)
            logger.info(f"Typed successfully in {locator}")
        except Exception as e:
            logger.error(f"[TYPE FAILED] {locator} text='{text}' → {e}")
            self._screenshot("type_failed")
            raise

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
    # 🔥 IS VISIBLE
    # -------------------------------------------------------------------
    def is_visible(self, locator):
        try:
            return self.wait(locator)
        except:
            return False

    # -------------------------------------------------------------------
    # 🔥 OPEN URL
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

    # existing code...

    def is_present(self, locator, timeout=3):
        """Return True if element is present, False otherwise"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
