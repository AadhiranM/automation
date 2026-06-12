from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage

class SAEnquirySendEmailPage(BasePage):

    # ---------------- INPUTS ----------------

    TO_EMAIL = (
        By.CSS_SELECTOR,
        "input[type='email']"
    )

    SUBJECT = (
        By.ID,
        "subject"
    )

    BODY = (
        By.XPATH,
        "//div[contains(@class,'ck-editor__editable') and @contenteditable='true']"
    )

    SEND_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Send']"
    )

    LATEST_EMAIL_BODY = (
        By.XPATH,
        "//ul[@id='followup-comment-list']/li[1]"
    )
    # ---------------- VALIDATION ERRORS ----------------

    SUBJECT_ERROR = (
        By.ID,
        "subject_error"
    )

    BODY_ERROR = (
        By.ID,
        "content_error"
    )

    # ---------------- TOAST ----------------

    SUCCESS_TOAST = (
        By.XPATH,
        "//div[contains(@class,'toastify')]"
    )

    # ---------------- PREVIOUS EMAIL SECTION ----------------

    PREVIOUS_EMAIL_SECTION = (
        By.XPATH,
        "//h5[normalize-space()='Previous Email']"
    )

    PREV_EMAIL_SENDERS = (
        By.XPATH,
        "//ul[@id='followup-comment-list']//strong"
    )

    PREV_EMAIL_DATES = (
        By.XPATH,
        "//ul[@id='followup-comment-list']//span[contains(@class,'comment-meta')]"
    )

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
        "(//ul[@id='followup-comment-list']/li[1]//div[contains(@class,'prev_mail_txt')])[1]"
    )

    PREV_EMAIL_BODY = (
        By.XPATH,
        "//ul[@id='followup-comment-list']/li[1]//div[contains(@class,'comment-body')]"
    )

    # =====================================================
    # INPUT METHODS
    # =====================================================

    def latest_email_contains(
            self,
            expected_text
    ):

        return (
                expected_text
                in
                self.get_text(
                    self.LATEST_EMAIL_BODY
                )
        )

    def type_subject(self, text):

        self.type(
            self.SUBJECT,
            text
        )

    def type_body(self, text):

        editor = self.is_visible(
            self.BODY
        )

        editor.click()

        editor.send_keys(
            Keys.CONTROL,
            "a"
        )

        editor.send_keys(
            Keys.DELETE
        )

        editor.send_keys(
            text
        )

    def click_send(self):

        self.click(
            self.SEND_BUTTON
        )

    # =====================================================
    # ERROR METHODS
    # =====================================================

    def wait_subject_error(self):

        return self.is_visible(
            self.SUBJECT_ERROR
        )

    def wait_body_error(self):

        return self.is_visible(
            self.BODY_ERROR
        )

    # =====================================================
    # TOAST
    # =====================================================

    def get_toast_text(self):

        toast = self.wait(
            self.SUCCESS_TOAST
        )

        return toast.text.strip()

    # =====================================================
    # REUSABLE SEND EMAIL
    # =====================================================

    def send_email(
            self,
            subject,
            body
    ):

        self.type_subject(
            subject
        )

        self.type_body(
            body
        )

        self.click_send()

        return self.get_toast_text()

    # =====================================================
    # EMAIL HISTORY
    # =====================================================

    def wait_for_email_history_refresh(self):

        WebDriverWait(
            self.driver,
            20
        ).until(
            lambda d:
            len(
                d.find_elements(
                    *self.PREV_EMAIL_SUBJECT
                )
            ) > 0
        )

    def get_previous_email_details(self):

        return {

            "sender":
                self.get_text(
                    self.PREV_EMAIL_SENDER
                ).strip(),

            "date":
                self.get_text(
                    self.PREV_EMAIL_DATE
                ).strip(),

            "subject":
                self.get_text(
                    self.PREV_EMAIL_SUBJECT
                ).strip(),

            "body":
                self.get_text(
                    self.PREV_EMAIL_BODY
                ).strip()
        }

    def verify_latest_email(
            self,
            expected_subject,
            expected_body
    ):

        details = (
            self.get_previous_email_details()
        )

        assert (
            expected_subject
            in
            details["subject"]
        )

        assert (
            expected_body
            ==
            details["body"]
        )

        assert (
            "Superadmin"
            in
            details["sender"]
        )

        return details

    # =====================================================
    # VALIDATIONS
    # =====================================================

    def is_email_disabled(self):

        el = self.wait(
            self.TO_EMAIL
        )

        return (
            el.get_attribute(
                "readonly"
            )
            or
            not el.is_enabled()
        )

    def is_previous_email_section_present(self):

        return self.is_visible(
            self.PREVIOUS_EMAIL_SECTION
        )

    def latest_email_exists(self):

        return bool(
            self.driver.find_elements(
                *self.PREV_EMAIL_SUBJECT
            )
        )

    # =====================================================
    # DATE VALIDATION
    # =====================================================

    def get_all_previous_senders(self):

        elements = (
            self.driver.find_elements(
                *self.PREV_EMAIL_SENDERS
            )
        )

        return [
            e.text.strip()
            for e in elements
        ]

    def get_all_previous_dates(self):

        elements = (
            self.driver.find_elements(
                *self.PREV_EMAIL_DATES
            )
        )

        return [
            e.text.strip()
            for e in elements
        ]

    def is_valid_date_format(
            self,
            date_text
    ):

        try:

            datetime.strptime(
                date_text,
                "%b %d, %Y at %I:%M %p"
            )

            return True

        except ValueError:

            return False

    def validate_all_email_dates(self):

        dates = (
            self.get_all_previous_dates()
        )

        for date_text in dates:

            assert (
                self.is_valid_date_format(
                    date_text
                )
            )