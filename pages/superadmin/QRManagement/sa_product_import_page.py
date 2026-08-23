import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


# =========================================================
# TEST DATA
# =========================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

PRODUCT_IMPORT_FILE = os.path.join(
    BASE_DIR,
    "test_data",
    "excel",
    "1784091129_product_import_beta_jul15.xlsx"
)


class SAProductImportPage(BasePage):

    # =========================================================
    # PRODUCT LIST
    # =========================================================

    IMPORT_BTN = (
        By.XPATH,
        "//button[normalize-space()='Import']"
    )

    FILE_STATUS = (
        By.ID,
        "fileStatus"
    )

    IMPORT_LOGS_BTN = (
        By.XPATH,
        "//button[normalize-space()='Import Logs']"
    )

    FIRST_MANUFACTURER = (
        By.XPATH,
        "//table/tbody/tr[1]/td[3]"
    )

    # =========================================================
    # IMPORT MODAL - STEP 1
    # =========================================================

    IMPORT_MODAL = (
        By.XPATH,
        "//div[contains(@class,'modal') and "
        ".//h5[contains(normalize-space(),'Import Products')]]"
    )

    CONTINUE_BTN = (
        By.XPATH,
        "//div[contains(@class,'modal') and "
        ".//h5[contains(normalize-space(),'Import Products')]]"
        "//button[normalize-space()='Continue']"
    )

    DOWNLOAD_TEMPLATE_BTN = (
        By.XPATH,
        "//button[contains(normalize-space(),'Download Sample Template')]"
    )

    # =========================================================
    # IMPORT MODAL - STEP 2
    # =========================================================

    FILE_INPUT = (
        By.ID,
        "fileInput"
    )

    MANUFACTURER_DROPDOWN = (
        By.XPATH,
        "//select[@id='import-manufacturer-select']"
        "/ancestor::div[contains(@class,'choices')]"
        "//div[contains(@class,'choices__inner')]"
    )

    IMPORT_SUBMIT_BTN = (
        By.XPATH,
        "//div[contains(@class,'modal')]"
        "//button[normalize-space()='Import']"
    )

    # =========================================================
    # TOAST
    # =========================================================

    TOAST_MSG = (
        By.XPATH,
        "//div[contains(@class,'toastify')]"
    )

    # =========================================================
    # IMPORT LOGS
    # =========================================================

    IMPORT_LOGS_TITLE = (
        By.XPATH,
        "//h5[contains(normalize-space(),'Import Logs')]"
    )

    FIRST_LOG_ROW = (
        By.XPATH,
        "//table/tbody/tr[1]"
    )

    FIRST_LOG_STATUS = (
        By.XPATH,
        "//table/tbody/tr[1]/td[7]"
    )

    SUCCESS_STATUS = (
        By.XPATH,
        "//table/tbody/tr[1]/td[7]"
        "//span[normalize-space()='Success']"
    )

    PENDING_STATUS = (
        By.XPATH,
        "//table/tbody/tr[1]/td[7]"
        "//span[normalize-space()='Pending']"
    )

    # =========================================================
    # NAVIGATION
    # =========================================================

    def goto_product_page(self):

        self.driver.get(
            "https://beta.digitathya.com/admin/product?reset_filters=1"
        )

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                self.IMPORT_BTN
            )
        )

    def goto_import_logs(self):

        self.driver.get(
            "https://beta.digitathya.com/admin/"
            "import-logs?type=product&reset_filters=1"
        )

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                self.IMPORT_LOGS_TITLE
            )
        )

    # =========================================================
    # PRODUCT LIST
    # =========================================================

    def get_first_manufacturer(self):

        return self.get_text(
            self.FIRST_MANUFACTURER
        ).strip()

    def open_import(self):

        self.click(self.IMPORT_BTN)

        continue_button = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[normalize-space()='Continue']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            continue_button
        )

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[normalize-space()='Continue']"
                )
            )
        )

        continue_button.click()

    # =========================================================
    # IMPORT STEP 1
    # =========================================================

    def click_continue(self):

        continue_locator = (
            By.XPATH,
            "//button[normalize-space()='Continue']"
        )

        continue_button = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.element_to_be_clickable(
                continue_locator
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            continue_button
        )

        print("Clicked Continue")

    # =========================================================
    # FILE UPLOAD
    # =========================================================

    def upload_product_excel(self):

        if not os.path.exists(PRODUCT_IMPORT_FILE):
            raise FileNotFoundError(
                f"Product import file not found: {PRODUCT_IMPORT_FILE}"
            )

        file_input = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.presence_of_element_located(
                (By.ID, "fileInput")
            )
        )

        file_input.send_keys(PRODUCT_IMPORT_FILE)

        # IMPORTANT:
        # Do NOT proceed until application itself says Upload Completed.
        WebDriverWait(
            self.driver,
            60
        ).until(
            EC.text_to_be_present_in_element(
                (By.ID, "fileStatus"),
                "Upload Completed"
            )
        )

        print("Product Excel upload completed.")

    # =========================================================
    # MANUFACTURER
    # =========================================================

    def select_manufacturer(self, manufacturer_name):

        # Open the visible Choices.js dropdown
        dropdown = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.element_to_be_clickable(
                self.MANUFACTURER_DROPDOWN
            )
        )

        dropdown.click()

        # Select the visible manufacturer option
        option = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'choices__list--dropdown')]"
                    "//div[contains(@class,'choices__item--selectable')]"
                    "[normalize-space()='{}']".format(
                        manufacturer_name
                    )
                )
            )
        )

        option.click()

        print(
            f"Manufacturer selected: {manufacturer_name}"
        )

        # ============================================================
        # IMPORTANT:
        # Wait until Choices.js updates the REAL <select>
        # ============================================================

        WebDriverWait(
            self.driver,
            10
        ).until(
            lambda d: d.find_element(
                By.ID,
                "import-manufacturer-select"
            ).get_attribute("value") not in (None, "")
        )

        manufacturer_select = self.driver.find_element(
            By.ID,
            "import-manufacturer-select"
        )

        print(
            "Actual select value:",
            manufacturer_select.get_attribute("value")
        )

        # ============================================================
        # FORCE THE SAME CHANGE EVENT USED BY THE APPLICATION
        # ============================================================

        self.driver.execute_script(
            """
            const select = arguments[0];

            select.dispatchEvent(
                new Event('change', {
                    bubbles: true
                })
            );

            select.dispatchEvent(
                new Event('input', {
                    bubbles: true
                })
            );
            """,
            manufacturer_select
        )

        # ============================================================
        # IMPORTANT:
        # Give the application time to process the change event
        # ============================================================

        import_button = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'modal')]"
                    "//button[normalize-space()='import']"
                )
            )
        )

        # Wait for the application's button state
        WebDriverWait(
            self.driver,
            20
        ).until(
            lambda d: (
                    import_button.is_enabled()
                    and
                    import_button.get_attribute("disabled") is None
            )
        )

        print("Modal Import button is enabled.")

    # =========================================================
    # IMPORT
    # =========================================================

    def click_import(self):

        import_button = WebDriverWait(
            self.driver,
            30
        ).until(
            EC.element_to_be_clickable(
                self.IMPORT_BTN
            )
        )

        import_button.click()

        print("Import button clicked.")

    # =========================================================
    # TOAST
    # =========================================================

    def get_toast_message(self):

        toast = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                self.TOAST_MSG
            )
        )

        message = toast.text.strip()

        print(
            f"Toast Message: {message}"
        )

        return message

    # =========================================================
    # WAIT FOR IMPORT LOGS
    # =========================================================

    def wait_for_import_logs(self):

        WebDriverWait(
            self.driver,
            20
        ).until(
            EC.visibility_of_element_located(
                self.IMPORT_LOGS_TITLE
            )
        )

    # =========================================================
    # FIRST LOG STATUS
    # =========================================================

    def get_first_import_status(self):

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                self.FIRST_LOG_ROW
            )
        )

        return self.get_text(
            self.FIRST_LOG_STATUS
        ).strip()

    # =========================================================
    # WAIT UNTIL SUCCESS
    # =========================================================

    def wait_until_import_success(
            self,
            max_attempts=6,
            refresh_interval=5
    ):

        for attempt in range(1, max_attempts + 1):

            status = self.get_first_import_status()

            print(
                f"Import attempt {attempt}: "
                f"Status = {status}"
            )

            if status.lower() == "success":
                return True

            if status.lower() == "pending":

                if attempt < max_attempts:
                    time.sleep(refresh_interval)
                    self.driver.refresh()

                    WebDriverWait(
                        self.driver,
                        15
                    ).until(
                        EC.visibility_of_element_located(
                            self.IMPORT_LOGS_TITLE
                        )
                    )

                    continue

            return False

        return False