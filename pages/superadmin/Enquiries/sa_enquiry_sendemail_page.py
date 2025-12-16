from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.common.base_page import BasePage
from datetime import datetime


class SAEnquirySendEmailPage(BasePage):

    # ---------------- INPUT LOCATORS ----------------
    TO_EMAIL = (By.CSS_SELECTOR, "input[type='email']")
    PREVIOUS_EMAIL_SECTION = (By.XPATH, "//h5[normalize-space()='Previous Email']")

    PREV_EMAIL_SENDERS = (
        By.XPATH,
        "//ul[@id='followup-comment-list']//strong"
    )

    PREV_EMAIL_DATES = (
        By.XPATH,
        "//ul[@id='followup-comment-list']//span[contains(@class,'comment-meta')]"
    )

    SUBJECT = (By.ID, "subject")

    # CKEditor editable DIV
    BODY = (
        By.XPATH,
        "//div[contains(@class,'ck-editor__editable') and @contenteditable='true']"
    )

    SEND_BUTTON = (
        By.XPATH, "//button[normalize-space()='Submit']"
    )

    # ---------------- VALIDATION ERRORS ----------------
    SUBJECT_ERROR = (By.ID, "subject_error")
    BODY_ERROR = (By.ID, "content_error")

    # ---------------- TOAST / SUCCESS ----------------
    SUCCESS_TOAST = (
        By.XPATH,
        "//div[contains(@class,'toastify') and contains(text(),'Email')]"
    )

    # ---------------- PREVIOUS EMAIL (LATEST) ----------------
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
        "//ul[@id='followup-comment-list']/li[1]//div[@class='comment-body']"
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
    def get_toast_text(self):
        toast = self.wait(self.SUCCESS_TOAST)
        return toast.text.strip()

    # ---------------- PREVIOUS EMAIL EXTRACTION ----------------
    def get_previous_email_details(self):
        return {
            "sender": self.get_text(self.PREV_EMAIL_SENDER).strip(),
            "date": self.get_text(self.PREV_EMAIL_DATE).strip(),
            "subject": self.get_text(self.PREV_EMAIL_SUBJECT).strip(),
            "body": self.get_text(self.PREV_EMAIL_BODY).strip(),
        }

    # ---------------- VALIDATIONS ----------------
    def is_email_disabled(self):
        el = self.wait(self.TO_EMAIL)
        return el.get_attribute("readonly") or not el.is_enabled()

    def is_previous_email_section_present(self):
        return self.is_visible(self.PREVIOUS_EMAIL_SECTION)

    def get_all_previous_senders(self):
        elements = self.driver.find_elements(*self.PREV_EMAIL_SENDERS)
        return [e.text.strip() for e in elements]

    def get_all_previous_dates(self):
        elements = self.driver.find_elements(*self.PREV_EMAIL_DATES)
        return [e.text.strip() for e in elements]

    def is_valid_date_format(self, date_text):
        try:
            datetime.strptime(date_text, "%b %d, %Y at %I:%M %p")
            return True
        except ValueError:
            return False

