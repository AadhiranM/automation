from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage


class SAManufacturerInvitePage(BasePage):

    CONFIRM_BTN = (By.CSS_SELECTOR, "button.swal2-confirm")
    CANCEL_BTN = (By.CSS_SELECTOR, "button.swal2-cancel")
    SUCCESS_MSG = (By.XPATH, "//div[contains(text(),'Invitation')]")
    OK_BTN = (By.XPATH, "//button[normalize-space()='OK']")

    def confirm_send(self):
        self.click(self.CONFIRM_BTN)

    def cancel_send(self):
        self.click(self.CANCEL_BTN)

    def wait_for_success(self):
        self.wait(self.SUCCESS_MSG)

    def click_ok(self):
        self.click(self.OK_BTN)
