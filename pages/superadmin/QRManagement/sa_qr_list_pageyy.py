from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException
)

from pages.common.base_page import BasePage

import os
import glob


class SAQRListPage(BasePage):

    URL = "https://beta.digitathya.com/admin/qr-management?reset_filters=1"

    SEARCH_BOX = (
        By.XPATH,
        "//input[contains(@placeholder,'Search')]"
    )

    SEARCH_BTN = (
        By.XPATH,
        "//button[contains(@class,'search')]"
    )  # adjust if needed

    FIRST_ROW = (
        By.XPATH,
        "(//table//tbody/tr)[1]"
    )

    NO_DATA_ROW = (
        By.XPATH,
        "//td[contains(@class,'dataTables_empty')]"
    )

    # =========================
    # NAVIGATION
    # =========================

    FIRST_BATCH = (
        By.XPATH,
        "(//table//tbody//tr[1]//td)[4]"
    )

    def get_first_batch_text(self):
        return self.get_text(self.FIRST_BATCH)

    def goto_page(self):
        self.driver.get(self.URL)
        self.wait_for_results()

    # =========================
    # WAIT FOR TABLE
    # =========================

    def wait_for_results(self):
        WebDriverWait(self.driver, 15).until(
            lambda d: d.find_elements(*self.FIRST_ROW)
            or d.find_elements(*self.NO_DATA_ROW)
        )

    # =========================
    # SEARCH (SAME AS MANUFACTURER)
    # =========================

    def search_batch(self, batch):
        self.wait_for_results()

        self.type(self.SEARCH_BOX, batch)
        self.click(self.SEARCH_BTN)

        self.wait_for_results()

    # =========================
    # VALIDATION
    # =========================

    def is_batch_present(self, batch):
        rows = self.driver.find_elements(
            By.XPATH,
            f"//table//tbody//td[contains(text(),'{batch}')]"
        )

        return len(rows) > 0

    # =========================================================
    # NEW METHODS FOR QR LIFECYCLE
    # =========================================================

    # =========================
    # FIND BATCH ROW
    # =========================

    def _find_batch_row(self, batch):

        rows = self.driver.find_elements(
            By.XPATH,
            "//table//tbody/tr"
        )

        for row in rows:

            try:
                if batch in row.text:
                    return row

            except StaleElementReferenceException:
                continue

        return False

    # =========================
    # WAIT FOR GENERATED BATCH
    # =========================

    def wait_for_batch(
        self,
        batch,
        timeout=60
    ):

        print(
            f"Waiting for batch: {batch}"
        )

        def find_batch(driver):

            try:

                row = self._find_batch_row(
                    batch
                )

                return row if row else False

            except StaleElementReferenceException:
                return False

        row = WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=2
        ).until(
            find_batch
        )

        print(
            f"Batch found successfully: {batch}"
        )

        return row

    # =========================
    # GET BATCH STATUS
    # =========================

    def get_batch_status(self, batch):

        row = self.wait_for_batch(
            batch
        )

        # Status button is inside the row.
        # It contains values such as:
        # QR Generated
        # In Print
        # In Transit
        # Completed

        status_button = row.find_element(
            By.XPATH,
            ".//button["
            "normalize-space()='QR Generated' "
            "or normalize-space()='In Print' "
            "or normalize-space()='In Transit' "
            "or normalize-space()='Completed'"
            "]"
        )

        return status_button.text.strip()

    # =========================
    # WAIT FOR STATUS
    # =========================

    def wait_for_batch_status(
        self,
        batch,
        expected_status,
        timeout=60
    ):

        print(
            f"Waiting for batch '{batch}' "
            f"to become '{expected_status}'"
        )

        def check_status(driver):

            try:

                row = self._find_batch_row(
                    batch
                )

                if not row:
                    return False

                status_button = row.find_element(
                    By.XPATH,
                    ".//button["
                    "normalize-space()='QR Generated' "
                    "or normalize-space()='In Print' "
                    "or normalize-space()='In Transit' "
                    "or normalize-space()='Completed'"
                    "]"
                )

                actual_status = (
                    status_button.text.strip()
                )

                print(
                    f"Batch: {batch} | "
                    f"Current Status: {actual_status}"
                )

                return (
                    actual_status ==
                    expected_status
                )

            except (
                StaleElementReferenceException,
                TimeoutException
            ):
                return False

        WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=2
        ).until(
            check_status
        )

        print(
            f"Batch '{batch}' reached "
            f"status '{expected_status}'"
        )

    # =========================
    # VERIFY STATUS
    # =========================

    def verify_batch_status(
        self,
        batch,
        expected_status
    ):

        actual_status = self.get_batch_status(
            batch
        )

        assert actual_status == expected_status, (
            f"Status validation failed for batch "
            f"'{batch}'. "
            f"Expected='{expected_status}', "
            f"Actual='{actual_status}'"
        )

        print(
            f"Status validation passed: "
            f"{expected_status}"
        )

    # =========================================================
    # CHANGE STATUS
    # =========================================================

    def change_status(
        self,
        batch,
        new_status,
        comments="Test"
    ):

        # -----------------------------------------------------
        # 1. Find exact batch row
        # -----------------------------------------------------

        row = self.wait_for_batch(
            batch
        )

        # -----------------------------------------------------
        # 2. Find current status button
        # -----------------------------------------------------

        status_button = row.find_element(
            By.XPATH,
            ".//button["
            "normalize-space()='QR Generated' "
            "or normalize-space()='In Print' "
            "or normalize-space()='In Transit' "
            "or normalize-space()='Completed'"
            "]"
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            status_button
        )

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.element_to_be_clickable(
                status_button
            )
        )

        # -----------------------------------------------------
        # 3. Click current status
        # -----------------------------------------------------

        self.driver.execute_script(
            "arguments[0].click();",
            status_button
        )

        print(
            f"Status dropdown opened for batch: "
            f"{batch}"
        )

        # -----------------------------------------------------
        # 4. Click requested status
        # -----------------------------------------------------

        status_option = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'dropdown-menu') "
                    "and contains(@class,'show')]"
                    f"//*[normalize-space()="
                    f"'{new_status}']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            status_option
        )

        print(
            f"Selected status: {new_status}"
        )

        # -----------------------------------------------------
        # 5. Wait for confirmation modal
        # -----------------------------------------------------

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(normalize-space(),"
                    "'Are you sure you want to change "
                    "the status?')]"
                )
            )
        )

        # -----------------------------------------------------
        # 6. Enter comments
        # -----------------------------------------------------

        comments_box = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//textarea"
                )
            )
        )

        comments_box.clear()

        comments_box.send_keys(
            comments
        )

        # -----------------------------------------------------
        # 7. Click Update Status
        # -----------------------------------------------------

        update_button = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[normalize-space()='Update Status']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            update_button
        )

        print(
            f"Update Status clicked: {new_status}"
        )

        # -----------------------------------------------------
        # 8. Wait for modal to disappear
        # -----------------------------------------------------

        try:

            WebDriverWait(
                self.driver,
                15
            ).until(
                EC.invisibility_of_element_located(
                    (
                        By.XPATH,
                        "//*[contains(normalize-space(),"
                        "'Are you sure you want to change "
                        "the status?')]"
                    )
                )
            )

        except TimeoutException:

            print(
                "Warning: confirmation modal did not "
                "disappear within timeout."
            )

    # =========================================================
    # TRACKING VALIDATION
    # =========================================================

    def verify_tracking_status(
        self,
        batch,
        expected_status
    ):

        row = self.wait_for_batch(
            batch
        )

        # -----------------------------------------------------
        # Tracking section is inside the same batch row.
        #
        # The application shows tracking stages visually:
        #
        # Request Received
        # QR Generated
        # In Print
        # In Transit
        # Completed
        # -----------------------------------------------------

        # We look for elements inside the row that have
        # tooltip-related attributes/classes.

        tracking_elements = row.find_elements(
            By.XPATH,
            ".//*["
            "@title or "
            "@data-bs-title or "
            "@data-bs-original-title"
            "]"
        )

        found = False

        for element in tracking_elements:

            try:

                title = element.get_attribute(
                    "title"
                )

                if title and expected_status.lower() in title.lower():

                    print(
                        f"Tracking validation passed: "
                        f"{expected_status}"
                    )

                    found = True
                    break

                data_title = element.get_attribute(
                    "data-bs-title"
                )

                if (
                    data_title
                    and
                    expected_status.lower()
                    in data_title.lower()
                ):

                    print(
                        f"Tracking validation passed: "
                        f"{expected_status}"
                    )

                    found = True
                    break

                original_title = element.get_attribute(
                    "data-bs-original-title"
                )

                if (
                    original_title
                    and
                    expected_status.lower()
                    in original_title.lower()
                ):

                    print(
                        f"Tracking validation passed: "
                        f"{expected_status}"
                    )

                    found = True
                    break

            except StaleElementReferenceException:

                continue

        # -----------------------------------------------------
        # If tooltip is generated dynamically, hover over
        # tracking elements and inspect visible tooltip.
        # -----------------------------------------------------

        if not found:

            tracking_elements = row.find_elements(
                By.XPATH,
                ".//*["
                "contains(@class,'tracking') "
                "or contains(@class,'step') "
                "or contains(@class,'circle') "
                "or contains(@class,'rounded-circle')"
                "]"
            )

            for element in tracking_elements:

                try:

                    ActionChains(
                        self.driver
                    ).move_to_element(
                        element
                    ).perform()

                    tooltip = WebDriverWait(
                        self.driver,
                        2
                    ).until(
                        EC.visibility_of_element_located(
                            (
                                By.XPATH,
                                "//*["
                                "contains(@class,'tooltip') "
                                "and "
                                "not(contains(@style,"
                                "'display: none'))"
                                "]"
                            )
                        )
                    )

                    tooltip_text = (
                        tooltip.text.strip()
                    )

                    if (
                        expected_status.lower()
                        in tooltip_text.lower()
                    ):

                        print(
                            f"Tracking validation passed: "
                            f"{expected_status}"
                        )

                        found = True
                        break

                except (
                    TimeoutException,
                    StaleElementReferenceException
                ):

                    continue

        # -----------------------------------------------------
        # Final validation
        # -----------------------------------------------------

        assert found, (
            f"Tracking status '{expected_status}' "
            f"was not found for batch '{batch}'."
        )

    # =========================================================
    # DOWNLOAD BATCH
    # =========================================================

    def download_batch(
        self,
        batch
    ):

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

        # -----------------------------------------------------
        # Files present before download
        # -----------------------------------------------------

        before_files = set(
            glob.glob(
                os.path.join(
                    download_path,
                    "*"
                )
            )
        )

        # -----------------------------------------------------
        # Find exact batch row
        # -----------------------------------------------------

        row = self.wait_for_batch(
            batch
        )

        # -----------------------------------------------------
        # Download button
        #
        # Screenshot shows a dark blue button with
        # download icon + dropdown arrow.
        # -----------------------------------------------------

        download_button = row.find_element(
            By.XPATH,
            ".//button["
            ".//*[contains(@class,'download')] "
            "or contains(@title,'Download') "
            "or contains(@aria-label,'Download') "
            "or .//i[contains(@class,'download')]"
            "]"
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            download_button
        )

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.element_to_be_clickable(
                download_button
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            download_button
        )

        print(
            f"Download menu opened for batch: "
            f"{batch}"
        )

        # -----------------------------------------------------
        # Download Batch ZIP
        # -----------------------------------------------------

        download_option = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'dropdown-menu') "
                    "and contains(@class,'show')]"
                    "//*[normalize-space()='Download Batch ZIP']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            download_option
        )

        print(
            "Download Batch ZIP clicked."
        )

        # -----------------------------------------------------
        # Wait for ZIP
        # -----------------------------------------------------

        downloaded_file = WebDriverWait(
            self.driver,
            60,
            poll_frequency=1
        ).until(
            lambda d: self._get_new_zip_file(
                download_path,
                before_files
            )
        )

        print(
            f"Batch downloaded successfully: "
            f"{downloaded_file}"
        )

        return downloaded_file

    # =========================================================
    # FIND NEW ZIP FILE
    # =========================================================

    @staticmethod
    def _get_new_zip_file(
        download_path,
        before_files
    ):

        current_files = set(
            glob.glob(
                os.path.join(
                    download_path,
                    "*"
                )
            )
        )

        new_files = (
            current_files -
            before_files
        )

        for file_path in new_files:

            # Chrome temporary download
            if file_path.endswith(
                ".crdownload"
            ):
                continue

            # Only accept actual ZIP
            if file_path.lower().endswith(
                ".zip"
            ):
                return file_path

        return False