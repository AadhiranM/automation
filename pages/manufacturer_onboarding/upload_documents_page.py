from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage
import time


class UploadDocumentsPage(BasePage):

    # =====================================================
    # FILE INPUTS
    # =====================================================

    BUSINESS_PAN = (
        By.ID,
        "doc_1"
    )

    CERTIFICATE_OF_INCORP = (
        By.ID,
        "doc_2"
    )

    MOA = (
        By.ID,
        "doc_3"
    )

    BOARD_RESOLUTION = (
        By.ID,
        "doc_4"
    )

    # =====================================================
    # BUTTONS
    # =====================================================

    SUBMIT_BTN = (
        By.XPATH,
        "//button[normalize-space()='Submit Documents']"
    )

    # =====================================================
    # TOAST
    # =====================================================

    TOAST_BODY = (
        By.XPATH,
        "//div[contains(@class,'toast-body')]"
    )

    # =====================================================
    # PAGE LOAD
    # =====================================================
    FIELD_ERRORS = (By.CSS_SELECTOR, "div.invalid-feedback")

    def get_all_field_errors(self):
        elements = self.driver.find_elements(*self.FIELD_ERRORS)
        return [e.text.strip() for e in elements if e.text.strip()]

    def wait_for_page(self):

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                self.BUSINESS_PAN
            )
        )

    # =====================================================
    # INTERNAL FILE WAIT
    # =====================================================

    def _upload_file(self, locator, path):

        file_input = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.presence_of_element_located(locator)
        )

        file_input.send_keys(path)

        WebDriverWait(
            self.driver,
            10
        ).until(
            lambda d:
            d.find_element(*locator).get_attribute("value") != ""
        )

        print(
            f"Uploaded: "
            f"{path.split('/')[-1]}"
        )

    # =====================================================
    # UPLOAD METHODS
    # =====================================================

    def upload_business_pan(self, path):

        self._upload_file(
            self.BUSINESS_PAN,
            path
        )

    def upload_certificate(self, path):

        self._upload_file(
            self.CERTIFICATE_OF_INCORP,
            path
        )

    def upload_moa(self, path):

        self._upload_file(
            self.MOA,
            path
        )

    def upload_board_resolution(self, path):

        self._upload_file(
            self.BOARD_RESOLUTION,
            path
        )

    # =====================================================
    # VERIFY ALL FILES SELECTED
    # =====================================================

    def verify_all_files_selected(self):

        fields = [
            self.BUSINESS_PAN,
            self.CERTIFICATE_OF_INCORP,
            self.MOA,
            self.BOARD_RESOLUTION
        ]

        for field in fields:

            value = self.driver.find_element(
                *field
            ).get_attribute(
                "value"
            )

            assert value != "", \
                f"File not selected: {field}"

        print(
            "All 4 files selected"
        )

    # =====================================================
    # WAIT FOR UI PROCESSING
    # =====================================================

    def wait_for_upload_processing(self):

        time.sleep(5)

    # =====================================================
    # SUBMIT
    # =====================================================

    def submit(self):

        btn = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.element_to_be_clickable(
                self.SUBMIT_BTN
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        # Wait until onboarding page redirects to manufacturer list
        WebDriverWait(
            self.driver,
            60
        ).until(
            lambda d: "/admin/manufacturer" in d.current_url
        )

        WebDriverWait(
            self.driver,
            60
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[contains(@placeholder,'Search')]"
                )
            )
        )

    # =====================================================
    # RESULT
    # =====================================================

    def wait_and_get_result(
            self,
            timeout=20
    ):

        end_time = (
            time.time() + timeout
        )

        while time.time() < end_time:

            toast = self.driver.execute_script("""
                let t =
                document.querySelector(
                    '.toast.show .toast-body'
                );
                return t ? t.innerText : null;
            """)

            if toast:

                toast = toast.strip()

                print(
                    "TOAST:",
                    toast
                )

                if "success" in toast.lower():

                    return (
                        "SUCCESS",
                        toast
                    )

                return (
                    "ERROR",
                    toast
                )

            time.sleep(0.5)

        return (
            "UNKNOWN",
            "No toast appeared"
        )
    def goto_upload_tab(self):
        self.click((By.XPATH, "//a[normalize-space()='Upload Document']"))

    def click_submit_only(self):
        """
        Use this for NEGATIVE tests where submission is expected to fail.
        Unlike submit(), this does NOT wait for a success redirect —
        it just clicks and returns immediately.
        """
        self.click(self.SUBMIT_BTN)