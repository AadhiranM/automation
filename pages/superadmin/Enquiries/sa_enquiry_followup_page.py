from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.common.base_page import BasePage


class SAEnquiryFollowUpPage(BasePage):

    # ---------------- INPUT FIELD (CKEditor) ----------------
    BODY = (
        By.XPATH,
        "//div[contains(@class,'ck-editor__editable') and @contenteditable='true']"
    )

    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")

    # ---------------- SUCCESS TOAST ----------------
    SUCCESS_TOAST = (
        By.XPATH,
        "//div[contains(@class,'toastify') and contains(text(),'success')]"
    )

    # ---------------- PREVIOUS FOLLOW-UP SECTION ----------------
    FIRST_FOLLOWUP_CARD = (
        By.XPATH,
        "(//ul[contains(@class,'list-group')]//li)[1]"
    )

    FOLLOWUP_SENDER = (
        By.XPATH,
        "(//ul[contains(@class,'list-group')]//li)[1]//strong"
    )

    FOLLOWUP_TIME = (
        By.XPATH,
        "(//ul[contains(@class,'list-group')]//li)[1]//span[contains(@class,'comment-meta')]"
    )

    FOLLOWUP_TEXT = (
        By.XPATH,
        "(//ul[contains(@class,'list-group')]//li)[1]//p"
    )

    # ---------------- METHODS ----------------
    def type_followup(self, text):
        """Safe CKEditor typing."""
        editor = self.is_visible(self.BODY)
        editor.click()
        editor.send_keys(Keys.CONTROL, "a")
        editor.send_keys(Keys.DELETE)
        editor.send_keys(text)

    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)

    def wait_for_success(self):
        """Wait for success toast (auto screenshot handled by BasePage)."""
        return self.is_visible(self.SUCCESS_TOAST)

    def get_latest_followup(self):
        """Return dict → sender, time, message"""
        return {
            "sender": self.get_text(self.FOLLOWUP_SENDER).strip(),
            "time": self.get_text(self.FOLLOWUP_TIME).strip(),
            "message": self.get_text(self.FOLLOWUP_TEXT).strip(),
        }
