import os
import time
import glob
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

INVALID_IMAGE_FILE = os.path.join(
    BASE_DIR,
    "test_data",
    "images",
    "importimg.jpeg"
)

INVALID_PDF_FILE = os.path.join(
    BASE_DIR,
    "test_data",
    "images",
    "importpdf.pdf"
)

# =========================================================
# IMPORT LOG ACTIONS
# =========================================================

# =========================================================
# IMPORT LOG ACTIONS
# =========================================================



class SAProductImportPage(BasePage):

    # =========================================================
    # PRODUCT LIST
    # =========================================================

    IMPORT_BTN = (
        By.XPATH,
        "//button[normalize-space()='Import']"
    )

    FIRST_LOG_ACTION_BTN = (
        By.XPATH,
        "//table[@id='crudTable']/tbody/tr[1]/td[last()]//button"
    )

    UPLOADED_FILE_OPTION = (
        By.XPATH,
        "//ul[contains(@class,'dropdown-menu') and contains(@class,'show')]"
        "//a[normalize-space()='Uploaded File']"
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

    # =========================================================
    # INVALID FILE VALIDATION
    # =========================================================

    INVALID_FILE_MESSAGE = (
        By.XPATH,
        "//*[contains(normalize-space(.),"
        "'Invalid file format. Please upload an Excel (.xlsx) file only.')]"
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
        "//button[normalize-space()='import']"
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

        # Upload the Excel file
        file_input.send_keys(PRODUCT_IMPORT_FILE)

        # Wait until application shows upload completed
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

        # IMPORTANT:
        # The application clears the native file input after processing.
        # Re-attach the file so the application's form state sees the file.
        WebDriverWait(
            self.driver,
            10
        ).until(
            lambda d: d.find_element(
                By.ID,
                "fileInput"
            ).is_enabled()
        )

        file_input = self.driver.find_element(
            By.ID,
            "fileInput"
        )

        file_input.send_keys(PRODUCT_IMPORT_FILE)

        print("Product Excel file re-attached to file input.")

    # =========================================================
    # MANUFACTURER
    # =========================================================

    # =========================================================
    # INVALID FILE UPLOAD
    # =========================================================

    def upload_invalid_product_file(self, file_path):

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Invalid test file not found: {file_path}"
            )

        file_input = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.presence_of_element_located(
                self.FILE_INPUT
            )
        )

        file_input.send_keys(file_path)

        print(
            f"Invalid file uploaded: {file_path}"
        )

        WebDriverWait(
            self.driver,
            60
        ).until(
            EC.text_to_be_present_in_element(
                self.FILE_STATUS,
                "Upload Completed"
            )
        )

        print("Invalid file upload completed.")

        # Re-attach, same as positive Excel flow
        file_input = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                self.FILE_INPUT
            )
        )

        file_input.send_keys(file_path)

        print(
            "Invalid file re-attached to file input."
        )

    def get_invalid_file_message(self):

        message = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                self.INVALID_FILE_MESSAGE
            )
        )

        text = message.text.strip()

        print(
            f"Invalid File Message: {text}"
        )

        return text

    def select_manufacturer(self, manufacturer_name):

        # 1. Open Choices.js dropdown
        dropdown = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.element_to_be_clickable(self.MANUFACTURER_DROPDOWN)
        )

        dropdown.click()

        # 2. Click the actual Choices.js option
        option = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'choices__list--dropdown')]"
                    "//div[contains(@class,'choices__item--selectable')]"
                    "[normalize-space()=" + repr(manufacturer_name) + "]"
                )
            )
        )

        option.click()

        # 3. Verify that the underlying select really contains TATA
        WebDriverWait(
            self.driver,
            10
        ).until(
            lambda d: d.find_element(
                By.ID,
                "import-manufacturer-select"
            ).get_attribute("value") != ""
        )

        selected_value = self.driver.find_element(
            By.ID,
            "import-manufacturer-select"
        ).get_attribute("value")

        print(
            f"Manufacturer selected: {manufacturer_name}"
        )
        print(
            f"Manufacturer value: {selected_value}"
        )

        # 4. IMPORTANT:
        # Give the application's change/upload state time to update.
        import_button = WebDriverWait(
            self.driver,
            30
        ).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'modal')"
                    " and .//*[contains(text(),'Upload Completed')]]"
                    "//button[normalize-space()='import']"
                )
            )
        )

        # 5. Wait for the APPLICATION to enable the button
        WebDriverWait(
            self.driver,
            30
        ).until(
            lambda d: import_button.get_attribute("disabled") is None
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
                self.IMPORT_SUBMIT_BTN
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

    def download_uploaded_file(self):

        worker = os.getenv(
            "PYTEST_XDIST_WORKER",
            "master"
        )

        download_path = os.path.join(
            os.getcwd(),
            "downloads",
            worker
        )

        os.makedirs(
            download_path,
            exist_ok=True
        )

        before_files = set(
            glob.glob(
                os.path.join(
                    download_path,
                    "*"
                )
            )
        )

        # =====================================================
        # STEP 1 - CLICK THREE DOTS
        # =====================================================

        action_button = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.element_to_be_clickable(
                self.FIRST_LOG_ACTION_BTN
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            action_button
        )

        print("Import log action menu opened.")

        # =====================================================
        # STEP 2 - CLICK UPLOADED FILE
        # =====================================================

        uploaded_file = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.element_to_be_clickable(
                self.UPLOADED_FILE_OPTION
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            uploaded_file
        )

        print("Uploaded File clicked.")

        # =====================================================
        # STEP 3 - WAIT FOR DOWNLOAD
        # =====================================================

        downloaded_file = WebDriverWait(
            self.driver,
            30
        ).until(
            lambda driver: next(
                (
                    file
                    for file in glob.glob(
                    os.path.join(
                        download_path,
                        "*.xlsx"
                    )
                )
                    if file not in before_files
                ),
                False
            )
        )

        print(
            f"Uploaded file downloaded successfully: "
            f"{downloaded_file}"
        )