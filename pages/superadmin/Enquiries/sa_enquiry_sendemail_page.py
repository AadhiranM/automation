from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.common.base_page import BasePage


class SAEnquirySendEmailPage(BasePage):

    # ---------------- INPUT LOCATORS ----------------
    TO_EMAIL = (By.ID, "email-to")
    SUBJECT = (By.ID, "subject")

    # CKEditor editable DIV
    BODY = (
        By.XPATH,
        "//div[contains(@class,'ck-editor__editable') and @contenteditable='true']"
    )

    SEND_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Submit') or contains(text(),'Send')]"
    )

    # ---------------- VALIDATION ERRORS ----------------
    SUBJECT_ERROR = (By.ID, "subject_error")
    BODY_ERROR = (By.ID, "content_error")

    # ---------------- TOAST / SUCCESS ----------------
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class,'toastify') and contains(text(),'Email')]")

    # ---------------- PREVIOUS EMAIL SECTION ----------------
    PREV_EMAIL_SENDER = (
        By.XPATH,
        "//ul[@id='followup-comment-list']/li[1]//strong"
    )

    PREV_EMAIL_DATE = (
        By.XPATH,
        "//ul[@id='followup-comment-list']/li[1]//span[contains(@class,'comment-meta')]"
    )

    PREV_EMAIL_SUBJECT = (
        By.XPATH,
        "//ul[@id='followup-comment-list']/li[1]//div[contains(@class,'fw-semibold')]"
    )

    PREV_EMAIL_BODY = (
        By.XPATH,
        "//ul[@id='followup-comment-list']/li[1]//div[@class='comment-body']/p"
    )

    # ---------------- INPUT METHODS ----------------
    def type_subject(self, text):
        self.type(self.SUBJECT, text)

    def type_body(self, text):
        """CKEditor body is a contenteditable DIV (not iframe)."""
        editor = self.is_visible(self.BODY)
        editor.click()
        editor.send_keys(Keys.CONTROL, "a")
        editor.send_keys(Keys.DELETE)
        editor.send_keys(text)

    def click_send(self):
        self.click(self.SEND_BUTTON)

    # ---------------- ERROR WAIT METHODS ----------------
    def wait_subject_error(self):
        return self.is_visible(self.SUBJECT_ERROR)

    def wait_body_error(self):
        return self.is_visible(self.BODY_ERROR)

    # ---------------- TOAST ----------------
    def wait_for_toast(self):
        return self.is_visible(self.SUCCESS_TOAST)

    # ---------------- PREVIOUS EMAIL EXTRACTION ----------------
    def get_previous_email_details(self):
        return {
            "sender": self.get_text(self.PREV_EMAIL_SENDER).strip(),
            "date": self.get_text(self.PREV_EMAIL_DATE).strip(),
            "subject": self.get_text(self.PREV_EMAIL_SUBJECT).strip(),
            "body": self.get_text(self.PREV_EMAIL_BODY).strip(),
        }
