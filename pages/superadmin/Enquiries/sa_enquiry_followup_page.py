from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from pages.common.base_page import BasePage


class SAEnquiryFollowUpPage(BasePage):

    # ---------------- INPUT FIELD (CKEditor) ----------------
    # ----------------- ACTION MENU ITEMS -----------------


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

    LATEST_FOLLOWUP_CARD = (
        By.XPATH,
        "(//ul[contains(@class,'list-group')]//li)[1]"
    )



    # Validation error
    CONTENT_ERROR = (By.ID, "content_error")

    # ---------------- METHODS ----------------
    def wait_for_followup_refresh(
            self,
            expected_message
    ):
        WebDriverWait(
            self.driver,
            20
        ).until(
            lambda d:
            expected_message in
            d.find_element(
                *self.LATEST_FOLLOWUP_CARD
            ).text
        )

    def latest_followup_contains(
            self,
            expected_text
    ):
        card_text = self.get_text(
            self.LATEST_FOLLOWUP_CARD
        )

        return (
                expected_text
                in
                card_text
        )

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


    def get_toast_text(self):
        toast = self.wait(self.SUCCESS_TOAST)
        return toast.text.strip()

    def wait_for_content_error(self):
        return self.is_visible(self.CONTENT_ERROR)
