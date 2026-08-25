from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException
)
import requests
from pages.common.base_page import BasePage
import os
import time
from pathlib import Path

class SAQRListPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.download_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "tests",
                "superadmin",
                "QRManagement",
                "reports",
                "downloads",
                "master"
            )
        )

        os.makedirs(
            self.download_dir,
            exist_ok=True
        )

    URL = "https://beta.digitathya.com/admin/qr-management?reset_filters=1"

    SEARCH_BOX = (
        By.XPATH,
        "//input[contains(@placeholder,'Search')]"
    )

    SEARCH_BTN = (
        By.XPATH,
        "//button[contains(@class,'search')]"
    )

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

    def wait_for_page(self):
        self.wait_for_results()

    # =========================
    # WAIT FOR TABLE
    # =========================

    def wait_for_results(self):
        WebDriverWait(
            self.driver,
            15
        ).until(
            lambda d:
            d.find_elements(*self.FIRST_ROW)
            or d.find_elements(*self.NO_DATA_ROW)
        )

    # =========================
    # SEARCH
    # =========================

    def search_batch(self, batch):

        self.wait_for_results()

        self.type(
            self.SEARCH_BOX,
            batch
        )

        self.click(
            self.SEARCH_BTN
        )

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

    # =========================
    # FIND BATCH ROW
    # =========================

    def _get_batch_row(self, batch):

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

        return None

    # =========================
    # WAIT FOR BATCH
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

                row = self._get_batch_row(
                    batch
                )

                if row:
                    return row

                return False

            except StaleElementReferenceException:
                return False

        row = WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=2
        ).until(find_batch)

        print(
            f"Batch found: {batch}"
        )

        return row

    # =========================
    # GET BATCH STATUS
    # =========================

    def get_batch_status(self, batch):

        row = self.wait_for_batch(
            batch
        )

        status_button = row.find_element(
            By.XPATH,
            ".//button["
            "contains(normalize-space(.),"
            "'QR Generated') "
            "or contains(normalize-space(.),"
            "'In Print') "
            "or contains(normalize-space(.),"
            "'In Transit') "
            "or contains(normalize-space(.),"
            "'Completed')"
            "]"
        )

        return status_button.text.strip()

    # =========================
    # WAIT FOR BATCH STATUS
    # =========================

    def wait_for_batch_status(
        self,
        batch,
        expected_status,
        timeout=60
    ):

        print(
            f"Waiting for batch "
            f"{batch} -> {expected_status}"
        )

        def check_status(driver):

            try:

                row = self._get_batch_row(
                    batch
                )

                if not row:
                    return False

                status_button = row.find_element(
                    By.XPATH,
                    ".//button["
                    "contains(normalize-space(.),"
                    "'QR Generated') "
                    "or contains(normalize-space(.),"
                    "'In Print') "
                    "or contains(normalize-space(.),"
                    "'In Transit') "
                    "or contains(normalize-space(.),"
                    "'Completed')"
                    "]"
                )

                actual_status = (
                    status_button.text.strip()
                )

                print(
                    f"Batch: {batch} | "
                    f"Expected: {expected_status} | "
                    f"Actual: {actual_status}"
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
        ).until(check_status)

        print(
            f"Batch {batch} reached "
            f"status: {expected_status}"
        )

    # =========================
    # VERIFY BATCH STATUS
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
            f"Batch status validation failed. "
            f"Expected: {expected_status}, "
            f"Actual: {actual_status}"
        )

        print(
            f"Batch status validation passed: "
            f"{expected_status}"
        )

    # =====================================================
    # GET STATUS BUTTON LOCATOR
    # =====================================================

    def _get_status_button_locator(self, batch):

        return (
            By.XPATH,
            f"//table//tbody//tr["
            f".//td[contains(normalize-space(),'{batch}')]"
            f"]//button[contains(@class,'tracker_status_dropdown')]"
        )

    # =====================================================
    # CHANGE STATUS
    # =====================================================

    def change_status(
            self,
            batch,
            new_status,
            comments="Test"
    ):

        print(
            f"Changing batch {batch} "
            f"to {new_status}"
        )

        # =================================================
        # STEP 1 - WAIT FOR BATCH
        # =================================================

        self.wait_for_batch(
            batch
        )

        # =================================================
        # STEP 2 - STATUS BUTTON LOCATOR
        #
        # IMPORTANT:
        # Do NOT store the WebElement here.
        # The table can refresh/re-render and make
        # previously found elements stale.
        # =================================================

        status_locator = (
            By.XPATH,
            f"//table//tbody//tr["
            f".//td[contains(normalize-space(), "
            f"'{batch}')]"
            f"]//button[contains("
            f"@class, "
            f"'tracker_status_dropdown'"
            f")]"
        )

        # =================================================
        # STEP 3 - WAIT FOR STATUS BUTTON
        # =================================================

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.presence_of_element_located(
                status_locator
            )
        )

        print(
            "Status dropdown button found"
        )

        # =================================================
        # STEP 4 - SCROLL TO STATUS BUTTON
        # =================================================

        def scroll_to_status_button(driver):

            try:

                button = driver.find_element(
                    *status_locator
                )

                driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });
                    """,
                    button
                )

                return True

            except StaleElementReferenceException:
                return False

        WebDriverWait(
            self.driver,
            15
        ).until(
            scroll_to_status_button
        )

        # =================================================
        # STEP 5 - CLICK STATUS DROPDOWN
        #
        # IMPORTANT:
        # Re-find the button on EVERY attempt.
        # This prevents stale element failures.
        # =================================================

        def click_status_dropdown(driver):

            try:

                # ALWAYS get a fresh element
                button = driver.find_element(
                    *status_locator
                )

                # Scroll fresh element
                driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });
                    """,
                    button
                )

                # Get fresh element AGAIN because scrolling
                # can trigger DOM updates in some applications.
                button = driver.find_element(
                    *status_locator
                )

                # Normal Selenium click first
                button.click()

                return True

            except (
                    StaleElementReferenceException,
                    ElementClickInterceptedException
            ):

                return False

        print(
            "Clicking tracker status dropdown"
        )

        WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.3
        ).until(
            click_status_dropdown
        )

        # =================================================
        # STEP 6 - VERIFY DROPDOWN REALLY OPENED
        #
        # Do NOT assume click succeeded.
        # Bootstrap adds "show" to the UL when opened.
        # =================================================

        dropdown_locator = (
            By.XPATH,
            "//ul[contains("
            "@class,"
            "'status-dropdown-menu'"
            ") and contains("
            "@class,"
            "'show'"
            ")]"
        )

        try:

            WebDriverWait(
                self.driver,
                10,
                poll_frequency=0.2
            ).until(
                EC.visibility_of_element_located(
                    dropdown_locator
                )
            )

        except TimeoutException:

            print(
                "Status dropdown did not open "
                "after first click. Retrying..."
            )

            # =================================================
            # FALLBACK CLICK
            #
            # Re-find the element again.
            # Never reuse the old WebElement.
            # =================================================

            def javascript_click_dropdown(driver):

                try:

                    button = driver.find_element(
                        *status_locator
                    )

                    driver.execute_script(
                        """
                        arguments[0].scrollIntoView({
                            block: 'center',
                            inline: 'center'
                        });
                        """,
                        button
                    )

                    button = driver.find_element(
                        *status_locator
                    )

                    driver.execute_script(
                        "arguments[0].click();",
                        button
                    )

                    return True

                except (
                        StaleElementReferenceException,
                        ElementClickInterceptedException
                ):

                    return False

            WebDriverWait(
                self.driver,
                10,
                poll_frequency=0.3
            ).until(
                javascript_click_dropdown
            )

            WebDriverWait(
                self.driver,
                10,
                poll_frequency=0.2
            ).until(
                EC.visibility_of_element_located(
                    dropdown_locator
                )
            )

        print(
            "Status dropdown actually opened"
        )

        # =================================================
        # STEP 7 - FIND REQUESTED STATUS
        # =================================================

        option_locator = (
            By.XPATH,
            f"//ul[contains("
            f"@class,"
            f"'status-dropdown-menu'"
            f") and contains("
            f"@class,"
            f"'show'"
            f")]"
            f"//a[contains("
            f"@class,"
            f"'status-change-trigger'"
            f") and "
            f"normalize-space(@data-status-label)="
            f"'{new_status}']"
        )

        # =================================================
        # STEP 8 - WAIT FOR STATUS OPTION
        # =================================================

        def get_status_option(driver):

            try:

                elements = driver.find_elements(
                    *option_locator
                )

                for element in elements:

                    try:

                        if (
                                element.is_displayed()
                                and element.is_enabled()
                        ):
                            return element

                    except StaleElementReferenceException:
                        continue

            except StaleElementReferenceException:
                pass

            return False

        status_option = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.2
        ).until(
            get_status_option
        )

        # =================================================
        # STEP 9 - CLICK NEXT STATUS
        # =================================================

        def click_status_option(driver):

            try:

                # Re-find option every attempt
                elements = driver.find_elements(
                    *option_locator
                )

                for element in elements:

                    try:

                        if (
                                element.is_displayed()
                                and element.is_enabled()
                        ):

                            driver.execute_script(
                                """
                                arguments[0].scrollIntoView({
                                    block: 'center',
                                    inline: 'center'
                                });
                                """,
                                element
                            )

                            # Re-find after scroll
                            elements = driver.find_elements(
                                *option_locator
                            )

                            for fresh_element in elements:

                                try:

                                    if (
                                            fresh_element.is_displayed()
                                            and fresh_element.is_enabled()
                                    ):
                                        fresh_element.click()

                                        return True

                                except StaleElementReferenceException:
                                    continue

                    except StaleElementReferenceException:
                        continue

            except StaleElementReferenceException:
                pass

            return False

        WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.2
        ).until(
            click_status_option
        )

        print(
            f"Selected status: {new_status}"
        )

        # =================================================
        # STEP 10 - WAIT FOR CONFIRMATION POPUP
        # =================================================

        confirmation_locator = (
            By.XPATH,
            "//*[contains("
            "normalize-space(),"
            "'Are you sure you want to change "
            "the status?')]"
        )

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                confirmation_locator
            )
        )

        print(
            "Status confirmation popup opened"
        )

        # =================================================
        # STEP 11 - COMMENTS
        # =================================================

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

        print(
            f"Comment entered: {comments}"
        )

        # =================================================
        # STEP 12 - UPDATE STATUS
        # =================================================

        update_button_locator = (
            By.XPATH,
            "//button["
            "normalize-space()='Update Status'"
            "]"
        )

        update_button = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.element_to_be_clickable(
                update_button_locator
            )
        )

        try:

            update_button.click()

        except (
                StaleElementReferenceException,
                ElementClickInterceptedException
        ):

            update_button = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.element_to_be_clickable(
                    update_button_locator
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                update_button
            )

        print(
            f"Update Status clicked: "
            f"{new_status}"
        )

        # =================================================
        # STEP 13 - WAIT FOR STATUS UPDATE
        # =================================================

        print(
            f"Waiting for batch {batch} "
            f"to reach status: {new_status}"
        )

        self.wait_for_batch_status(
            batch,
            new_status
        )

        print(
            f"Status update completed: "
            f"{new_status}"
        )

    def update_batch_status(
        self,
        batch,
        new_status,
        comments="Test"
    ):

        self.change_status(
            batch,
            new_status,
            comments
        )

    # =========================
    # VERIFY TRACKING STATUS
    # =========================

    # =========================
    # VERIFY TRACKING STATUS
    # =========================

    # =====================================================
    # VERIFY TRACKING STATUS
    # =====================================================

    def verify_tracking_status(
            self,
            batch,
            expected_status
    ):
        """
        Validate the lifecycle status of a QR batch.

        The status dropdown is used as the primary
        source of truth instead of relying on the
        tracking-icon tooltip.

        Expected lifecycle:

            Request Received
                    ↓
            QR Generated
                    ↓
               In Print
                    ↓
               In Transit
                    ↓
               Completed
        """

        print(
            f"Checking tracking status for batch: {batch}"
        )

        # =====================================================
        # STATUS CELL
        # =====================================================

        STATUS_CELL = (
            By.XPATH,
            "./td[9]"
        )

        # =====================================================
        # GET FRESH ROW
        # =====================================================

        def get_fresh_row(driver):

            rows = driver.find_elements(
                By.XPATH,
                "//table//tbody//tr"
            )

            for row in rows:

                try:

                    if not row.is_displayed():
                        continue

                    row_text = row.text.strip()

                    if batch.lower() in row_text.lower():
                        return row

                except StaleElementReferenceException:
                    continue

            return False

        row = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.3
        ).until(
            get_fresh_row
        )

        print(
            f"Batch found for tracking validation: "
            f"{batch}"
        )

        # =====================================================
        # ALWAYS RE-FIND STATUS CELL
        # =====================================================

        try:

            status_cell = row.find_element(
                *STATUS_CELL
            )

        except StaleElementReferenceException:

            row = WebDriverWait(
                self.driver,
                10,
                poll_frequency=0.3
            ).until(
                get_fresh_row
            )

            status_cell = row.find_element(
                *STATUS_CELL
            )

        # =====================================================
        # GET CURRENT STATUS TEXT
        # =====================================================

        current_status = (
                status_cell.text or ""
        ).strip()

        print(
            f"Batch: {batch} | "
            f"Expected tracking status: "
            f"{expected_status} | "
            f"Actual: {current_status}"
        )

        # =====================================================
        # VALIDATE STATUS
        # =====================================================

        assert expected_status.lower() in (
            current_status.lower()
        ), (
            f"Tracking status validation failed. "
            f"Expected: {expected_status}. "
            f"Actual: {current_status}. "
            f"Batch: {batch}"
        )

        print(
            f"Tracking status validation passed: "
            f"{expected_status}"
        )

        return True

    # =========================
    # DOWNLOAD BATCH
    # =========================

    def download_batch(self, batch):

        print(
            f"Starting downloads for batch: {batch}"
        )

        self.wait_for_batch(batch)

        print(
            f"Download directory: "
            f"{self.download_dir}"
        )

        os.makedirs(
            self.download_dir,
            exist_ok=True
        )

        # ================================================
        # DOWNLOAD BATCH ZIP
        # ================================================

        batch_zip = self._download_from_menu(
            batch=batch,
            menu_text="Download Batch ZIP",
            file_name=f"{batch}_batch.zip"
        )

        # ================================================
        # DOWNLOAD PDF ZIP
        # ================================================

        pdf_zip = self._download_from_menu(
            batch=batch,
            menu_text="Download PDF ZIP",
            file_name=f"{batch}_pdf.zip"
        )

        print(
            f"All downloads completed for batch: {batch}"
        )

        return (
            batch_zip,
            pdf_zip
        )

    def _download_from_menu(
            self,
            batch,
            menu_text,
            file_name
    ):
        print(
            f"Preparing download: {menu_text}"
        )

        # =================================================
        # STEP 1 - FIND FRESH BATCH ROW
        # =================================================

        self.wait_for_batch(batch)

        row = WebDriverWait(
            self.driver,
            15
        ).until(
            lambda driver: next(
                (
                    r
                    for r in driver.find_elements(
                    By.XPATH,
                    "//table//tbody//tr"
                )
                    if batch.lower() in r.text.lower()
                ),
                False
            )
        )

        print(
            f"Fresh row found: {batch}"
        )

        # =================================================
        # STEP 2 - FIND FRESH DOWNLOAD BUTTON
        # =================================================

        download_button = WebDriverWait(
            self.driver,
            15
        ).until(
            lambda driver: row.find_element(
                By.XPATH,
                ".//button[contains(@class,'tracker_dropdown')]"
            )
        )

        # =================================================
        # STEP 3 - MAKE SURE DROPDOWN IS CLOSED
        # =================================================

        aria_expanded = download_button.get_attribute(
            "aria-expanded"
        )

        if aria_expanded == "true":
            print(
                "Download dropdown already open - closing it"
            )

            self.driver.execute_script(
                "arguments[0].click();",
                download_button
            )

            WebDriverWait(
                self.driver,
                10
            ).until(
                lambda driver: (
                        download_button.get_attribute(
                            "aria-expanded"
                        ) == "false"
                )
            )

            print(
                "Download dropdown closed"
            )

        # =================================================
        # STEP 4 - RE-FIND BUTTON
        # Angular can refresh the DOM
        # =================================================

        row = WebDriverWait(
            self.driver,
            15
        ).until(
            lambda driver: next(
                (
                    r
                    for r in driver.find_elements(
                    By.XPATH,
                    "//table//tbody//tr"
                )
                    if batch.lower() in r.text.lower()
                ),
                False
            )
        )

        download_button = row.find_element(
            By.XPATH,
            ".//button[contains(@class,'tracker_dropdown')]"
        )

        # =================================================
        # STEP 5 - OPEN DROPDOWN
        # =================================================

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            download_button
        )

        # Re-find after scroll
        download_button = row.find_element(
            By.XPATH,
            ".//button[contains(@class,'tracker_dropdown')]"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            download_button
        )

        # =================================================
        # STEP 6 - WAIT FOR DROPDOWN TO ACTUALLY OPEN
        # =================================================

        menu_xpath = (
            "//ul[contains(@class,'tracker_dropdown-menu') "
            "and contains(@class,'show')]"
        )

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    menu_xpath
                )
            )
        )

        print(
            "Download dropdown actually opened"
        )

        # =================================================
        # STEP 7 - FIND THE REQUIRED OPTION
        # =================================================

        option_xpath = (
            f"{menu_xpath}"
            f"//a[contains(@class,'dropdown-item') "
            f"and normalize-space()='{menu_text}']"
        )

        download_link = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    option_xpath
                )
            )
        )

        # =================================================
        # STEP 8 - GET URL
        # =================================================

        download_url = download_link.get_attribute(
            "href"
        )

        if not download_url:
            raise AssertionError(
                f"Download URL not found: {menu_text}"
            )

        print(
            f"Download URL: {download_url}"
        )

        # =================================================
        # STEP 9 - CLOSE DROPDOWN
        #
        # IMPORTANT:
        # We are NOT clicking the download link because
        # the actual download is handled through requests.
        # Therefore we MUST close the UI dropdown ourselves.
        # =================================================

        # Re-find fresh button
        row = WebDriverWait(
            self.driver,
            15
        ).until(
            lambda driver: next(
                (
                    r
                    for r in driver.find_elements(
                    By.XPATH,
                    "//table//tbody//tr"
                )
                    if batch.lower() in r.text.lower()
                ),
                False
            )
        )

        download_button = row.find_element(
            By.XPATH,
            ".//button[contains(@class,'tracker_dropdown')]"
        )

        if download_button.get_attribute(
                "aria-expanded"
        ) == "true":
            print(
                "Closing download dropdown"
            )

            self.driver.execute_script(
                "arguments[0].click();",
                download_button
            )

            WebDriverWait(
                self.driver,
                10
            ).until(
                lambda driver: (
                        driver.find_element(
                            By.XPATH,
                            ".//button[contains(@class,'tracker_dropdown')]"
                        ).get_attribute(
                            "aria-expanded"
                        ) == "false"
                )
            )

            print(
                "Download dropdown closed"
            )

        # =================================================
        # STEP 10 - CREATE REQUEST SESSION
        # =================================================

        session = requests.Session()

        for cookie in self.driver.get_cookies():
            session.cookies.set(
                cookie["name"],
                cookie["value"],
                domain=cookie.get("domain"),
                path=cookie.get("path", "/")
            )

        # =================================================
        # STEP 11 - DOWNLOAD FILE
        # =================================================

        response = session.get(
            download_url,
            stream=True,
            timeout=60
        )

        print(
            f"Download response: {response.status_code}"
        )

        if response.status_code != 200:
            raise AssertionError(
                f"Download failed: {menu_text} | "
                f"HTTP {response.status_code}"
            )

        # =================================================
        # STEP 12 - SAVE FILE
        # =================================================

        file_path = os.path.join(
            self.download_dir,
            file_name
        )

        with open(
                file_path,
                "wb"
        ) as file:

            for chunk in response.iter_content(
                    chunk_size=8192
            ):

                if chunk:
                    file.write(chunk)

        # =================================================
        # STEP 13 - VERIFY
        # =================================================

        if not os.path.exists(file_path):
            raise AssertionError(
                f"File was not downloaded: {file_path}"
            )

        file_size = os.path.getsize(
            file_path
        )

        if file_size == 0:
            raise AssertionError(
                f"Downloaded file is empty: {file_path}"
            )

        print(
            f"Downloaded successfully: {file_path}"
        )

        print(
            f"File size: {file_size} bytes"
        )

        return file_path