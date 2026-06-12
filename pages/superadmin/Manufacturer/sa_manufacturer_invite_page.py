from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class SAManufacturerInvitePage(BasePage):

    # ---------------- CONFIRMATION POPUP ----------------

    CONFIRM_BTN = (
        By.CSS_SELECTOR,
        "button.swal2-confirm"
    )

    CANCEL_BTN = (
        By.CSS_SELECTOR,
        "button.swal2-cancel"
    )

    # ---------------- SUCCESS POPUP ----------------

    SUCCESS_TITLE = (
        By.XPATH,
        "//h2[contains(text(),'Invitation Sent')]"
    )

    OK_BTN = (
        By.XPATH,
        "//button[normalize-space()='OK']"
    )

    # =====================================================
    # ACTIONS
    # =====================================================

    def confirm_send(self):

        self.click(
            self.CONFIRM_BTN
        )

    def cancel_send(self):

        self.click(
            self.CANCEL_BTN
        )

    # =====================================================
    # VALIDATIONS
    # =====================================================

    def wait_for_success(self):

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                self.SUCCESS_TITLE
            )
        )

    def click_ok(self):

        self.click(
            self.OK_BTN
        )

    def invite_manufacturer(self):

        self.confirm_send()

        self.wait_for_success()

        self.click_ok()

    def is_confirmation_closed(self):

        try:

            WebDriverWait(
                self.driver,
                5
            ).until(
                EC.invisibility_of_element_located(
                    self.CONFIRM_BTN
                )
            )

            return True

        except TimeoutException:

            return False