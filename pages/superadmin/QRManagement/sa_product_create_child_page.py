from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SAProductCreateChildPage(BasePage):

    # =========================
    # UNIQUE ELEMENT (PAGE LOAD)
    # =========================
    PAGE_LOADED = (
        By.XPATH,
        "//button[contains(text(),'Continue to Video Details')]"
    )

    # =========================
    # VARIANT (FIX LATER IF NEEDED)
    # =========================
    VARIANT_TYPE = (
        By.XPATH,
        "//div[contains(text(),'Select Variant Type')]"
    )

    VARIANT_VALUE = (
        By.XPATH,
        "(//div[contains(text(),'Select Variant')])[2]"
    )

    CONTINUE_BTN = (
        By.XPATH,
        "//button[contains(text(),'Continue to Video Details')]"
    )

    # =========================
    # PAGE LOAD
    # =========================
    def wait_for_page(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.PAGE_LOADED)
        )

    # =========================
    # TEMP (SKIP COMPLEX VARIANT)
    # =========================
    def select_variant(self):
        print("Skipping variant selection for now")

    # =========================
    # NEXT STEP
    # =========================
    def go_to_video(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONTINUE_BTN)
        ).click()