from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SAManufacturerInvitePage(BasePage):

    CONFIRM_BTN = (By.CSS_SELECTOR, "button.swal2-confirm")
    CANCEL_BTN = (By.CSS_SELECTOR, "button.swal2-cancel")

    SUCCESS_TITLE = (
        By.XPATH,
        "//h2[contains(text(),'Invitation Sent')]"
    )

    OK_BTN = (By.XPATH, "//button[normalize-space()='OK']")

    def confirm_send(self):
        self.click(self.CONFIRM_BTN)

    def cancel_send(self):
        self.click(self.CANCEL_BTN)

    def wait_for_success(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUCCESS_TITLE)
        )

    def click_ok(self):
        self.click(self.OK_BTN)
