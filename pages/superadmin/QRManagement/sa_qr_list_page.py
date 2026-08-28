from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException
)
import requests
from pages.common.base_page import BasePage
import os
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
)
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys



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

    def _get_batch_row(self, batch_no, timeout=30):
        """
        Always find a fresh table row for the given batch.
        Do not keep an old WebElement because the table refreshes
        after status/action changes.
        """

        row_xpath = (
            f"//tr[.//td[contains(normalize-space(), '{batch_no}')]]"
        )

        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, row_xpath)
            )
        )

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

        print(f"Searching for batch: {batch}")

        self.wait_for_results()

        # =====================================================
        # IMPORTANT:
        # Always clear the existing search value before entering
        # a new batch number. This is especially important after
        # Reassign because the QR list is reloaded/rendered again.
        # =====================================================

        search_box = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.3,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.visibility_of_element_located(
                self.SEARCH_BOX
            )
        )

        try:
            search_box.click()
            search_box.send_keys(Keys.CONTROL, "a")
            search_box.send_keys(Keys.BACKSPACE)
        except StaleElementReferenceException:
            search_box = WebDriverWait(
                self.driver,
                10,
                poll_frequency=0.3,
                ignored_exceptions=(
                    StaleElementReferenceException,
                )
            ).until(
                EC.visibility_of_element_located(
                    self.SEARCH_BOX
                )
            )

            search_box.click()
            search_box.send_keys(Keys.CONTROL, "a")
            search_box.send_keys(Keys.BACKSPACE)

        self.type(
            self.SEARCH_BOX,
            batch
        )

        # Make sure the input really contains this batch.
        WebDriverWait(
            self.driver,
            10,
            poll_frequency=0.2
        ).until(
            lambda d: (
                d.find_element(
                    *self.SEARCH_BOX
                ).get_attribute("value") or ""
            ).strip().lower() == batch.strip().lower()
        )

        self.click(
            self.SEARCH_BTN
        )

        print(
            f"Search button clicked for batch: {batch}"
        )

        # Wait specifically for the requested batch instead of merely
        # checking whether an old table row still exists.
        self.wait_for_batch(
            batch
        )

        print(
            f"Search completed for batch: {batch}"
        )

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

    def wait_for_batch(self, batch):

        print(f"Waiting for batch: {batch}")

        def find_batch(driver):

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
                        print(f"Batch found: {batch}")
                        return row

                except StaleElementReferenceException:
                    continue

            return False

        return WebDriverWait(
            self.driver,
            60,
            poll_frequency=0.5,
            ignored_exceptions=(StaleElementReferenceException,)
        ).until(find_batch)



    # =========================
    # GET BATCH STATUS
    # =========================

    def _get_fresh_batch_row(self, batch_no):

        rows = self.driver.find_elements(
            By.XPATH,
            "//table//tbody//tr"
        )

        for row in rows:

            try:
                if not row.is_displayed():
                    continue

                if batch_no.lower() in row.text.lower():
                    return row

            except StaleElementReferenceException:
                continue

        return None

    # =========================
    # WAIT FOR BATCH STATUS
    # =========================

    def wait_for_batch_status(self, batch_no, expected_status):

        print(
            f"Waiting for batch {batch_no} -> {expected_status}"
        )

        def check_status(driver):

            rows = driver.find_elements(
                By.XPATH,
                "//table//tbody//tr"
            )

            for row in rows:

                try:

                    if not row.is_displayed():
                        continue

                    row_text = row.text.strip()

                    if batch_no.lower() not in row_text.lower():
                        continue

                    # Re-read status from THIS fresh row
                    status_element = row.find_element(
                        By.XPATH,
                        ".//td[last()-1]"
                    )

                    actual_status = status_element.text.strip()

                    print(
                        f"Batch: {batch_no} | "
                        f"Expected: {expected_status} | "
                        f"Actual: {actual_status}"
                    )

                    if actual_status.lower() == expected_status.lower():
                        return True

                except StaleElementReferenceException:
                    continue

            return False

        WebDriverWait(
            self.driver,
            90,
            poll_frequency=0.5,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(check_status)

        print(
            f"Batch {batch_no} reached status: {expected_status}"
        )

    def get_batch_status(self, batch_no):

        print(f"Getting current status for: {batch_no}")

        def check_status(driver):

            try:

                row = self._get_fresh_batch_row(batch_no)

                if row is None:
                    return False

                # IMPORTANT:
                # This row was freshly obtained
                status_element = row.find_element(
                    By.XPATH,
                    ".//td[last()-1]"
                )

                status = status_element.text.strip()

                print(
                    f"Batch: {batch_no} | "
                    f"Current Status: {status}"
                )

                return status

            except StaleElementReferenceException:

                print(
                    f"Table refreshed while reading "
                    f"{batch_no}. Retrying..."
                )

                return False

        return WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.5
        ).until(check_status)

    # =========================
    # VERIFY BATCH STATUS
    # =========================

    def verify_batch_status(self, batch_no, expected_status):

        print(
            f"Verifying batch {batch_no} "
            f"expected status: {expected_status}"
        )

        def verify(driver):

            try:

                row = self._get_fresh_batch_row(batch_no)

                if row is None:
                    print(
                        f"Batch {batch_no} not found yet"
                    )
                    return False

                status_element = row.find_element(
                    By.XPATH,
                    ".//td[last()-1]"
                )

                actual_status = status_element.text.strip()

                print(
                    f"Batch: {batch_no} | "
                    f"Expected: {expected_status} | "
                    f"Actual: {actual_status}"
                )

                return (
                        actual_status.lower()
                        == expected_status.lower()
                )

            except StaleElementReferenceException:

                print(
                    "Table refreshed while validating. "
                    "Re-reading row..."
                )

                return False

        WebDriverWait(
            self.driver,
            30,
            poll_frequency=0.5
        ).until(verify)

        print(
            f"Batch status validation passed: "
            f"{batch_no} -> {expected_status}"
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

        # =================================================
        # STEP 11 - COMMENTS
        # =================================================

        comments_box_locator = (
            By.XPATH,
            "//div[contains(@class,'modal') and contains(@style,'display: block')]"
            "//textarea"
        )

        comments_box = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.3
        ).until(
            EC.visibility_of_element_located(
                comments_box_locator
            )
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center'
            });
            """,
            comments_box
        )

        comments_box.click()
        comments_box.clear()
        comments_box.send_keys(comments)

        print(
            f"Comment entered: {comments}"
        )

        # =================================================
        # =================================================
        # STEP 12 - UPDATE STATUS
        # =================================================

        update_button_locator = (
            By.XPATH,
            "//div[contains(@class,'modal') and contains(@style,'display: block')]"
            "//button[normalize-space()='Update Status']"
        )

        update_button = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.3
        ).until(
            EC.element_to_be_clickable(update_button_locator)
        )

        print(
            f"Clicking Update Status for: {new_status}"
        )

        update_button.click()

        print(
            f"Update Status clicked: {new_status}"
        )

        # =================================================
        # STEP 12A - WAIT FOR MODAL TO CLOSE
        # =================================================

        def modal_closed(driver):

            try:
                modals = driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class,'modal') and contains(@style,'display: block')]"
                )

                return not any(
                    modal.is_displayed()
                    for modal in modals
                )

            except StaleElementReferenceException:
                return True

        WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.3
        ).until(
            modal_closed
        )

        print("Status confirmation modal closed")

        # =================================================
        # STEP 12B - WAIT FOR PAGE TO SETTLE
        # =================================================

        WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.5
        ).until(
            lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        print("Page settled after status update")

        # =================================================
        # STEP 13 - RESEARCH / VERIFY UPDATED ROW
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
            f"Status update completed: {new_status}"
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

    def cancel_request(self, batch_no, comment):

        print(f"Starting Cancel Request: {batch_no}")

        # =====================================================
        # FIND FRESH ROW
        # =====================================================

        self.wait_for_batch(batch_no)

        row = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.3
        ).until(
            lambda d: d.find_element(
                By.XPATH,
                f"//table//tbody//tr[contains(., '{batch_no}')]"
            )
        )

        # =====================================================
        # THREE DOTS
        # =====================================================

        action_button = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.3
        ).until(
            lambda d: row.find_element(
                By.XPATH,
                ".//td[last()]//button"
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            action_button
        )

        WebDriverWait(
            self.driver,
            10,
            poll_frequency=0.3
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//table//tbody//tr[contains(., '{batch_no}')]//td[last()]//button"
                )
            )
        ).click()

        # =====================================================
        # VERIFY MENU IS ACTUALLY OPEN
        # =====================================================

        cancel_option = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.3
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//a[normalize-space()='Cancel Request']"
                )
            )
        )

        print("Three-dot menu actually opened")

        # =====================================================
        # CLICK CANCEL REQUEST
        # =====================================================

        WebDriverWait(
            self.driver,
            10,
            poll_frequency=0.3
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[normalize-space()='Cancel Request']"
                )
            )
        ).click()

        print("Cancel Request clicked")

        # =====================================================
        # WAIT FOR CANCEL COMMENT MODAL
        # =====================================================

        # =====================================================
        # CANCEL COMMENT
        # =====================================================

        comment_box = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.3
        ).until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    "cancelComments"
                )
            )
        )

        WebDriverWait(
            self.driver,
            10,
            poll_frequency=0.3
        ).until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "cancelComments"
                )
            )
        )

        comment_box.click()
        comment_box.clear()
        comment_box.send_keys(comment)

        print(
            f"Comment entered: {comment}"
        )

        # =====================================================
        # UPDATE STATUS
        # =====================================================

        # =====================================================
        # CANCEL CONFIRMATION BUTTON
        # =====================================================

        cancel_button = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.3
        ).until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "confirmCancelRequest"
                )
            )
        )

        cancel_button.click()

        print("Cancel confirmation clicked")
        # =====================================================
        # WAIT FOR FINAL STATUS
        # =====================================================

        self.wait_for_batch_status(
            batch_no,
            "Request Cancelled"
        )

        print(
            f"Cancel Request completed: {batch_no}"
        )
    def invalidate_qr(self, batch_no, comment):

        print(f"Starting Invalidate: {batch_no}")

        self.wait_for_batch(batch_no)

        row = self.driver.find_element(
            By.XPATH,
            f"//table//tbody//tr[contains(., '{batch_no}')]"
        )

        # Three dots
        action_button = row.find_element(
            By.XPATH,
            ".//td[last()]//button"
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            action_button
        )

        action_button.click()

        print("Three-dot menu opened")

        # Invalidate
        invalidate_option = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[normalize-space()='Invalidate']"
                )
            )
        )

        invalidate_option.click()

        print("Invalidate clicked")

        # Comment
        comment_box = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//textarea"
                )
            )
        )

        comment_box.clear()
        comment_box.send_keys(comment)

        print(f"Comment entered: {comment}")

        # Update Status
        update_button = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[normalize-space()='Update Status']"
                )
            )
        )

        update_button.click()

        print("Update Status clicked")

        self.wait_for_batch_status(
            batch_no,
            "QR Invalidated"
        )

        print(
            f"Invalidate completed: {batch_no}"
        )

    def get_batch_product_and_variant(self, batch_no):

        print(
            f"Getting Product and Variant for batch: {batch_no}"
        )

        def find_product_and_variant(driver):

            rows = driver.find_elements(
                By.XPATH,
                "//table//tbody//tr"
            )

            for row in rows:

                try:

                    if not row.is_displayed():
                        continue

                    row_text = row.text.strip()

                    if batch_no.lower() not in row_text.lower():
                        continue

                    # IMPORTANT:
                    # Read Product and Variant from the SAME
                    # fresh row that contains the batch.

                    product = row.find_element(
                        By.XPATH,
                        ".//td[3]"
                    ).text.strip()

                    variant = row.find_element(
                        By.XPATH,
                        ".//td[5]"
                    ).text.strip()

                    if not product:
                        return False

                    if not variant:
                        return False

                    print(
                        f"Current Product : {product}"
                    )

                    print(
                        f"Current Variant : {variant}"
                    )

                    return product, variant

                except StaleElementReferenceException:

                    # Angular/DataTables refreshed the row.
                    # Retry with a completely fresh row.
                    continue

            return False

        # IMPORTANT:
        # Do NOT search only once.
        # Keep reading fresh rows until the table settles.

        return WebDriverWait(
            self.driver,
            30,
            poll_frequency=0.5,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            find_product_and_variant
        )

    def get_different_product_and_variant(
            self,
            current_product,
            current_variant
    ):
        """
        Select a different Product and Variant in the Reassign QR modal.

        IMPORTANT:
        The Reassign popup can render the controls with either
        Select2 or Choices.js depending on the current frontend
        component state. Therefore this method deliberately supports
        BOTH DOM structures.

        The critical point is:
            Product selection -> frontend refreshes Variant
            -> Variant must be located again from the DOM
            -> then Variant is opened.
        """

        wait = WebDriverWait(
            self.driver,
            30,
            poll_frequency=0.3,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        )

        print("Selecting different Product and Variant")

        # =========================================================
        # STEP 1 - VERIFY REASSIGN MODAL
        # =========================================================

        modal_locator = (
            By.XPATH,
            "//div[contains(@class,'modal') "
            "and .//*[normalize-space()='Reassign QR']]"
        )

        wait.until(
            EC.visibility_of_element_located(modal_locator)
        )

        print("Reassign modal is OPEN")

        # =========================================================
        # STEP 2 - PRODUCT CONTROL
        #
        # Support Select2 + Choices.js.
        # =========================================================

        product_control_locator = (
            By.XPATH,
            "//div[contains(@class,'modal') "
            "and .//*[normalize-space()='Reassign QR']]"
            "//label[normalize-space()='Product']"
            "/following::span[contains(@class,'select2-selection--single')][1]"
            " | "
            "//div[contains(@class,'modal') "
            "and .//*[normalize-space()='Reassign QR']]"
            "//label[normalize-space()='Product']"
            "/following::div[contains(@class,'choices__inner')][1]"
        )

        print("Locating PRODUCT dropdown...")

        product_control = wait.until(
            EC.visibility_of_element_located(
                product_control_locator
            )
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            product_control
        )

        time.sleep(0.3)

        # Re-find after scroll.
        product_control = wait.until(
            EC.visibility_of_element_located(
                product_control_locator
            )
        )

        # =========================================================
        # STEP 3 - OPEN PRODUCT
        # =========================================================

        print("Clicking PRODUCT dropdown")

        try:
            ActionChains(
                self.driver
            ).move_to_element(
                product_control
            ).click().perform()
        except (
            StaleElementReferenceException,
            ElementClickInterceptedException
        ):
            product_control = wait.until(
                EC.visibility_of_element_located(
                    product_control_locator
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                product_control
            )

        # =========================================================
        # STEP 4 - DETERMINE WHICH DROPDOWN LIBRARY OPENED
        # =========================================================

        select2_open_locator = (
            By.XPATH,
            "//span[contains(@class,'select2-container--open')]"
        )

        choices_open_locator = (
            By.XPATH,
            "//div[contains(@class,'choices') "
            "and contains(@class,'is-open')]"
        )

        def get_open_dropdown_type(driver):
            try:
                select2 = [
                    x for x in driver.find_elements(
                        *select2_open_locator
                    )
                    if x.is_displayed()
                ]

                if select2:
                    return "select2"

                choices = [
                    x for x in driver.find_elements(
                        *choices_open_locator
                    )
                    if x.is_displayed()
                ]

                if choices:
                    return "choices"

            except StaleElementReferenceException:
                return False

            return False

        dropdown_type = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(get_open_dropdown_type)

        print(
            f"PRODUCT dropdown OPENED "
            f"using {dropdown_type}"
        )

        # =========================================================
        # STEP 5 - PRODUCT OPTIONS
        # =========================================================

        if dropdown_type == "select2":

            product_option_locator = (
                By.XPATH,
                "//span[contains(@class,'select2-container--open')]"
                "//li[@role='option' "
                "and not(contains(@class,'select2-results__message'))]"
            )

        else:

            product_option_locator = (
                By.XPATH,
                "//div[contains(@class,'choices') "
                "and contains(@class,'is-open')]"
                "//div[contains(@class,'choices__list--dropdown')]"
                "//*[contains(@class,'choices__item--choice') "
                "and not(contains(@class,'choices__item--disabled'))]"
            )

        def visible_product_options(driver):
            try:
                options = []

                for option in driver.find_elements(
                    *product_option_locator
                ):
                    try:
                        if (
                            option.is_displayed()
                            and option.text.strip()
                        ):
                            options.append(option)
                    except StaleElementReferenceException:
                        continue

                return options if options else False

            except StaleElementReferenceException:
                return False

        product_options = WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.3,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            visible_product_options
        )

        print(
            f"Product options found: {len(product_options)}"
        )

        # =========================================================
        # STEP 6 - SELECT DIFFERENT PRODUCT
        # =========================================================

        new_product = None

        for option in product_options:

            try:

                option_text = option.text.strip()

                if not option.is_displayed() or not option_text:
                    continue

                print(
                    f"Available Product : {option_text}"
                )

                product_name = option_text

                if "(" in product_name:
                    product_name = (
                        product_name.split("(", 1)[0].strip()
                    )

                if (
                    product_name.lower()
                    == current_product.strip().lower()
                ):
                    continue

                new_product = product_name

                print(
                    f"Selected different Product : "
                    f"{new_product}"
                )

                # Re-find option by visible text.
                if dropdown_type == "select2":

                    if "'" in option_text:
                        xpath_text = (
                            "concat(" +
                            ", ".join(
                                "'" + part + "'"
                                for part in option_text.split("'")
                            ) +
                            ")"
                        )
                    else:
                        xpath_text = f"'{option_text}'"

                    fresh_option_locator = (
                        By.XPATH,
                        "//span[contains(@class,'select2-container--open')]"
                        "//li[@role='option' "
                        "and not(contains(@class,'select2-results__message'))]"
                        f"[normalize-space()={xpath_text}]"
                    )

                else:

                    fresh_option_locator = (
                        By.XPATH,
                        "//div[contains(@class,'choices') "
                        "and contains(@class,'is-open')]"
                        "//div[contains(@class,'choices__list--dropdown')]"
                        f"//*[contains(@class,'choices__item--choice') "
                        f"and normalize-space()={repr(option_text)}]"
                    )

                fresh_option = WebDriverWait(
                    self.driver,
                    10,
                    poll_frequency=0.2,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.element_to_be_clickable(
                        fresh_option_locator
                    )
                )

                try:
                    fresh_option.click()
                except (
                    StaleElementReferenceException,
                    ElementClickInterceptedException
                ):
                    fresh_option = self.driver.find_element(
                        *fresh_option_locator
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        fresh_option
                    )

                print(
                    f"Product selected : {new_product}"
                )

                break

            except StaleElementReferenceException:
                continue

        if not new_product:
            raise AssertionError(
                "Could not find a different product. "
                f"Current Product: {current_product}"
            )

        # =========================================================
        # STEP 7 - WAIT FOR PRODUCT DROPDOWN TO CLOSE
        # =========================================================

        print(
            "Waiting for Product selection to complete..."
        )

        def product_dropdown_closed(driver):
            try:

                select2_open = any(
                    x.is_displayed()
                    for x in driver.find_elements(
                        *select2_open_locator
                    )
                )

                choices_open = any(
                    x.is_displayed()
                    for x in driver.find_elements(
                        *choices_open_locator
                    )
                )

                return not select2_open and not choices_open

            except StaleElementReferenceException:
                return False

        try:
            WebDriverWait(
                self.driver,
                10,
                poll_frequency=0.2,
                ignored_exceptions=(
                    StaleElementReferenceException,
                )
            ).until(
                product_dropdown_closed
            )
        except TimeoutException:
            pass

        # =========================================================
        # STEP 8 - WAIT FOR VARIANT CONTROL TO BE CREATED/ENABLED
        #
        # THIS IS THE IMPORTANT FIX.
        #
        # Do NOT use a previously located Variant element.
        # Product selection can destroy and recreate it.
        # =========================================================

        print(
            "Waiting for Variant dropdown after Product selection"
        )

        variant_control_locator = (
            By.XPATH,
            "//div[contains(@class,'modal') "
            "and .//*[normalize-space()='Reassign QR']]"
            "//label[normalize-space()='Variant SKU']"
            "/following::span[contains(@class,'select2-selection--single')][1]"
            " | "
            "//div[contains(@class,'modal') "
            "and .//*[normalize-space()='Reassign QR']]"
            "//label[normalize-space()='Variant SKU']"
            "/following::div[contains(@class,'choices__inner')][1]"
        )

        def find_variant_control(driver):
            try:

                elements = driver.find_elements(
                    *variant_control_locator
                )

                for element in elements:

                    try:

                        if not element.is_displayed():
                            continue

                        # The screenshot shows the Variant field
                        # can initially be disabled. Check the actual
                        # underlying select/container state instead
                        # of trusting the wrapper's is_enabled().
                        classes = (
                            element.get_attribute("class") or ""
                        ).lower()

                        aria_disabled = (
                            element.get_attribute("aria-disabled")
                            or ""
                        ).lower()

                        if (
                            "disabled" in classes
                            and aria_disabled == "true"
                        ):
                            continue

                        return element

                    except StaleElementReferenceException:
                        continue

            except StaleElementReferenceException:
                return False

            return False

        variant_control = WebDriverWait(
            self.driver,
            30,
            poll_frequency=0.3,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            find_variant_control
        )

        print(
            "Variant dropdown control FOUND"
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            variant_control
        )

        time.sleep(0.3)

        # =========================================================
        # STEP 9 - OPEN VARIANT
        # =========================================================

        print("Clicking VARIANT dropdown")

        def click_variant(driver):
            try:

                # ALWAYS locate a fresh control.
                elements = driver.find_elements(
                    *variant_control_locator
                )

                target = None

                for element in elements:

                    try:

                        if not element.is_displayed():
                            continue

                        classes = (
                            element.get_attribute("class") or ""
                        ).lower()

                        aria_disabled = (
                            element.get_attribute("aria-disabled")
                            or ""
                        ).lower()

                        if (
                            "disabled" in classes
                            and aria_disabled == "true"
                        ):
                            continue

                        target = element
                        break

                    except StaleElementReferenceException:
                        continue

                if target is None:
                    return False

                driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });
                    """,
                    target
                )

                time.sleep(0.2)

                # Re-find after scroll.
                elements = driver.find_elements(
                    *variant_control_locator
                )

                for element in elements:

                    try:

                        if not element.is_displayed():
                            continue

                        classes = (
                            element.get_attribute("class") or ""
                        ).lower()

                        aria_disabled = (
                            element.get_attribute("aria-disabled")
                            or ""
                        ).lower()

                        if (
                            "disabled" in classes
                            and aria_disabled == "true"
                        ):
                            continue

                        target = element
                        break

                    except StaleElementReferenceException:
                        continue

                if target is None:
                    return False

                try:
                    ActionChains(
                        driver
                    ).move_to_element(
                        target
                    ).click().perform()

                except (
                    StaleElementReferenceException,
                    ElementClickInterceptedException
                ):
                    # Fresh element + JS fallback.
                    elements = driver.find_elements(
                        *variant_control_locator
                    )

                    target = next(
                        (
                            element
                            for element in elements
                            if element.is_displayed()
                        ),
                        None
                    )

                    if target is None:
                        return False

                    driver.execute_script(
                        "arguments[0].click();",
                        target
                    )

                return True

            except StaleElementReferenceException:
                return False

        WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            click_variant
        )

        print(
            "VARIANT dropdown clicked"
        )

        # =========================================================
        # STEP 10 - VERIFY VARIANT DROPDOWN OPEN
        # =========================================================

        def variant_dropdown_open(driver):
            try:

                # Select2
                if any(
                    x.is_displayed()
                    for x in driver.find_elements(
                        *select2_open_locator
                    )
                ):
                    return "select2"

                # Choices
                if any(
                    x.is_displayed()
                    for x in driver.find_elements(
                        *choices_open_locator
                    )
                ):
                    return "choices"

            except StaleElementReferenceException:
                return False

            return False

        variant_dropdown_type = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            variant_dropdown_open
        )

        print(
            f"VARIANT dropdown OPENED "
            f"using {variant_dropdown_type}"
        )

        # =========================================================
        # STEP 11 - VARIANT OPTIONS
        # =========================================================

        if variant_dropdown_type == "select2":

            variant_option_locator = (
                By.XPATH,
                "//span[contains(@class,'select2-container--open')]"
                "//li[@role='option' "
                "and not(contains(@class,'select2-results__message'))]"
            )

        else:

            variant_option_locator = (
                By.XPATH,
                "//div[contains(@class,'choices') "
                "and contains(@class,'is-open')]"
                "//div[contains(@class,'choices__list--dropdown')]"
                "//*[contains(@class,'choices__item--choice') "
                "and not(contains(@class,'choices__item--disabled'))]"
            )

        def visible_variant_options(driver):
            try:

                options = []

                for option in driver.find_elements(
                    *variant_option_locator
                ):

                    try:

                        if (
                            option.is_displayed()
                            and option.text.strip()
                        ):
                            options.append(option)

                    except StaleElementReferenceException:
                        continue

                return options if options else False

            except StaleElementReferenceException:
                return False

        variant_options = WebDriverWait(
            self.driver,
            30,
            poll_frequency=0.3,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            visible_variant_options
        )

        print(
            f"Variant options found: "
            f"{len(variant_options)}"
        )

        # =========================================================
        # STEP 12 - SELECT DIFFERENT VARIANT
        # =========================================================

        new_variant = None

        for option in variant_options:

            try:

                option_text = option.text.strip()

                if (
                    not option.is_displayed()
                    or not option_text
                ):
                    continue

                print(
                    f"Available Variant : {option_text}"
                )

                if (
                    option_text.lower()
                    == current_variant.strip().lower()
                ):
                    continue

                new_variant = option_text

                print(
                    f"Selected different Variant : "
                    f"{new_variant}"
                )

                if "'" in option_text:
                    xpath_text = (
                        "concat(" +
                        ", ".join(
                            "'" + part + "'"
                            for part in option_text.split("'")
                        ) +
                        ")"
                    )
                else:
                    xpath_text = f"'{option_text}'"

                if variant_dropdown_type == "select2":

                    fresh_variant_locator = (
                        By.XPATH,
                        "//span[contains(@class,'select2-container--open')]"
                        "//li[@role='option' "
                        "and not(contains(@class,'select2-results__message'))]"
                        f"[normalize-space()={xpath_text}]"
                    )

                else:

                    fresh_variant_locator = (
                        By.XPATH,
                        "//div[contains(@class,'choices') "
                        "and contains(@class,'is-open')]"
                        "//div[contains(@class,'choices__list--dropdown')]"
                        f"//*[contains(@class,'choices__item--choice') "
                        f"and normalize-space()={xpath_text}]"
                    )

                fresh_variant = WebDriverWait(
                    self.driver,
                    10,
                    poll_frequency=0.2,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.element_to_be_clickable(
                        fresh_variant_locator
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'nearest'
                    });
                    """,
                    fresh_variant
                )

                try:
                    fresh_variant.click()
                except (
                    StaleElementReferenceException,
                    ElementClickInterceptedException
                ):
                    fresh_variant = self.driver.find_element(
                        *fresh_variant_locator
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        fresh_variant
                    )

                print(
                    f"Variant selected : {new_variant}"
                )

                break

            except StaleElementReferenceException:
                continue

        if not new_variant:
            raise AssertionError(
                "Could not find a different variant. "
                f"Current Variant: {current_variant}"
            )

        print("=" * 60)
        print(f"NEW PRODUCT : {new_product}")
        print(f"NEW VARIANT : {new_variant}")
        print("=" * 60)

        return new_product, new_variant

    def wait_for_reassignment_update(
            self,
            batch_no,
            expected_product,
            expected_variant,
            timeout=90
    ):
        """
        Wait for the Reassign API/backend update to finish before
        refreshing/searching the QR Management list.

        IMPORTANT:
        Reassign behaves like the QR status transitions in the
        QR-generation flow:

            Submit
                ↓
            backend processing
                ↓
            list/API refresh
                ↓
            updated Product + Variant

        Do NOT immediately refresh the page after Submit.
        A refresh can happen while the backend is still processing,
        which can make the UI temporarily show the previous state.

        Therefore:
            1. wait for the modal to close
            2. wait for the backend to settle
            3. open ONE fresh QR Management list page
            4. search the batch
            5. keep polling/searching on that page until Product +
               Variant match the expected values
        """

        print("=" * 60)
        print(
            f"WAITING FOR REASSIGN BACKEND UPDATE : [{batch_no}]"
        )
        print(
            f"Expected Product : {expected_product}"
        )
        print(
            f"Expected Variant : {expected_variant}"
        )
        print("=" * 60)

        # =========================================================
        # STEP 1 - IMPORTANT WAIT AFTER SUBMIT
        #
        # Same principle used for QR Generated -> In Print ->
        # In Transit -> Completed.
        #
        # Give the backend/API enough time to complete the
        # reassignment BEFORE causing a new page load.
        # =========================================================

        print(
            "Waiting for Reassign backend processing to settle..."
        )

        time.sleep(5)

        print(
            "Initial Reassign backend wait completed"
        )

        # =========================================================
        # STEP 2 - ONE FRESH QR MANAGEMENT PAGE LOAD
        #
        # Do NOT refresh repeatedly inside the polling loop.
        # Repeated navigation can interrupt the application while
        # Angular is still updating the batch.
        # =========================================================

        print(
            "Opening fresh QR Management list after backend wait..."
        )

        self.goto_page()
        self.wait_for_page()

        # Extra render wait after navigation.
        time.sleep(2)

        print(
            "Fresh QR Management list loaded"
        )

        deadline = time.time() + timeout
        attempt = 0

        last_product = None
        last_variant = None

        # =========================================================
        # STEP 3 - SEARCH/POLL WITHOUT PAGE NAVIGATION
        # =========================================================

        while time.time() < deadline:

            attempt += 1

            try:

                print(
                    f"Checking reassignment update "
                    f"(attempt {attempt})"
                )

                # Always issue a fresh search request, but do NOT
                # navigate away from the current list page.
                self.search_batch(batch_no)

                # Allow Angular/DataTables to finish rendering the
                # newly returned row before reading it.
                time.sleep(2)

                def read_updated_values(driver):

                    rows = driver.find_elements(
                        By.XPATH,
                        "//table//tbody//tr"
                    )

                    for row in rows:

                        try:

                            if not row.is_displayed():
                                continue

                            row_text = row.text.strip()

                            if (
                                batch_no.lower()
                                not in row_text.lower()
                            ):
                                continue

                            product = row.find_element(
                                By.XPATH,
                                ".//td[3]"
                            ).text.strip()

                            variant = row.find_element(
                                By.XPATH,
                                ".//td[5]"
                            ).text.strip()

                            if not product or not variant:
                                return False

                            return product, variant

                        except StaleElementReferenceException:
                            continue

                    return False

                result = WebDriverWait(
                    self.driver,
                    8,
                    poll_frequency=0.5,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    read_updated_values
                )

                last_product, last_variant = result

                print(
                    f"Reassign check: "
                    f"Product={last_product} | "
                    f"Variant={last_variant}"
                )

                # =================================================
                # STEP 4 - FINAL MATCH
                # =================================================

                if (
                    last_product.strip().lower()
                    == expected_product.strip().lower()
                    and
                    last_variant.strip().lower()
                    == expected_variant.strip().lower()
                ):

                    print("=" * 60)
                    print(
                        "REASSIGN UPDATE REFLECTED IN LIST"
                    )
                    print(
                        f"Product : {last_product}"
                    )
                    print(
                        f"Variant : {last_variant}"
                    )
                    print("=" * 60)

                    return True

                print(
                    "List still shows the previous "
                    "Product/Variant."
                )

                print(
                    "Waiting before the next search..."
                )

            except TimeoutException:

                print(
                    "Batch row was not ready after search. "
                    "Waiting before retry..."
                )

            except StaleElementReferenceException:

                print(
                    "Table refreshed while reading reassigned "
                    "values. Waiting before retry..."
                )

            # =====================================================
            # IMPORTANT WAIT BETWEEN RETRIES
            #
            # Do not immediately search again. This is the same
            # approach used for the QR status transition fix.
            # =====================================================

            time.sleep(3)

        raise AssertionError(
            "Reassignment was submitted, but the QR List did not "
            "reflect the new Product/Variant within "
            f"{timeout} seconds. "
            f"Expected Product: {expected_product} | "
            f"Expected Variant: {expected_variant} | "
            f"Last Product: {last_product} | "
            f"Last Variant: {last_variant}"
        )

    def reassign_qr(
            self,
            batch_no,
            new_product,
            new_variant
    ):
        """
        Submit the Reassign QR modal.

        IMPORTANT:
        get_different_product_and_variant() has ALREADY:
            1. opened the Product dropdown
            2. selected a different Product
            3. opened the Variant dropdown
            4. selected a different Variant

        Therefore this method MUST NOT click Product or Variant again.

        The previous implementation was reopening Product here. That
        caused the frontend Select2/Angular state to change and the
        submit flow to time out.

        This method only verifies that the Reassign modal is still open
        and clicks the Submit button.
        """

        print(
            f"Submitting Reassign for batch: {batch_no}"
        )

        # =========================================================
        # STEP 1 - REASSIGN MODAL MUST ALREADY BE OPEN
        # =========================================================

        modal_locator = (
            By.XPATH,
            "//div[contains(@class,'modal') "
            "and .//*[normalize-space()='Reassign QR']]"
        )

        wait = WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        )

        wait.until(
            EC.visibility_of_element_located(
                modal_locator
            )
        )

        print("Reassign modal is OPEN")

        # =========================================================
        # STEP 2 - DO NOT TOUCH PRODUCT / VARIANT
        #
        # They were selected by get_different_product_and_variant().
        #
        # Screenshot state should be:
        #
        # Product     : Mobile (...)
        # Variant SKU : M19533-PROB-MO-01-Black-128GB-8GB
        #
        # We only read the values for logging.
        # =========================================================

        product_value_locator = (
            By.XPATH,
            "//div[contains(@class,'modal') "
            "and .//*[normalize-space()='Reassign QR']]"
            "//label[normalize-space()='Product']"
            "/following::span[contains(@class,'select2-selection__rendered')][1]"
            " | "
            "//div[contains(@class,'modal') "
            "and .//*[normalize-space()='Reassign QR']]"
            "//label[normalize-space()='Product']"
            "/following::div[contains(@class,'choices__inner')][1]"
        )

        variant_value_locator = (
            By.XPATH,
            "//div[contains(@class,'modal') "
            "and .//*[normalize-space()='Reassign QR']]"
            "//label[normalize-space()='Variant SKU']"
            "/following::span[contains(@class,'select2-selection__rendered')][1]"
            " | "
            "//div[contains(@class,'modal') "
            "and .//*[normalize-space()='Reassign QR']]"
            "//label[normalize-space()='Variant SKU']"
            "/following::div[contains(@class,'choices__inner')][1]"
        )

        def read_visible_text(locator):
            try:
                elements = self.driver.find_elements(*locator)

                for element in elements:
                    try:
                        if element.is_displayed():
                            text = element.text.strip()

                            if text:
                                return text
                    except StaleElementReferenceException:
                        continue

            except StaleElementReferenceException:
                pass

            return ""

        selected_product = read_visible_text(
            product_value_locator
        )

        selected_variant = read_visible_text(
            variant_value_locator
        )

        print(
            f"Current selected Product in modal : "
            f"{selected_product or new_product}"
        )

        print(
            f"Current selected Variant in modal : "
            f"{selected_variant or new_variant}"
        )

        # =========================================================
        # STEP 3 - SUBMIT BUTTON
        #
        # IMPORTANT:
        # Find the button from the modal every time.
        # Never keep a WebElement while Angular is rendering.
        # =========================================================

        submit_locator = (
            By.XPATH,
            "//div[contains(@class,'modal') "
            "and .//*[normalize-space()='Reassign QR']]"
            "//button["
            "normalize-space()='Submit'"
            " or "
            "normalize-space(.)='Submit'"
            "]"
        )

        def find_submit_button(driver):
            try:
                elements = driver.find_elements(
                    *submit_locator
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
                return False

            return False

        submit_button = wait.until(
            find_submit_button
        )

        print("Reassign Submit button found and enabled")

        # =========================================================
        # STEP 4 - SCROLL + RE-FIND
        # =========================================================

        try:
            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'center'
                });
                """,
                submit_button
            )
        except StaleElementReferenceException:
            pass

        # Angular can rerender after scroll.
        submit_button = WebDriverWait(
            self.driver,
            10,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            find_submit_button
        )

        # =========================================================
        # STEP 5 - CLICK SUBMIT
        #
        # Normal Selenium click first.
        # If Angular rerenders the button at that exact moment,
        # re-find it and use JS click.
        # =========================================================

        print("Clicking Reassign Submit")

        try:

            submit_button.click()

        except (
            StaleElementReferenceException,
            ElementClickInterceptedException
        ):

            print(
                "Submit button changed during click. "
                "Re-finding fresh Submit button..."
            )

            submit_button = WebDriverWait(
                self.driver,
                10,
                poll_frequency=0.2,
                ignored_exceptions=(
                    StaleElementReferenceException,
                )
            ).until(
                find_submit_button
            )

            self.driver.execute_script(
                "arguments[0].click();",
                submit_button
            )

        print("Reassign Submit clicked successfully")

        # =========================================================
        # STEP 6 - VERIFY SUBMIT ACTION
        #
        # The modal should close after a successful submission.
        # Do NOT fail immediately if the application keeps it open
        # briefly while the API request is processing.
        # =========================================================

        def modal_closed(driver):
            try:

                elements = driver.find_elements(
                    *modal_locator
                )

                visible = [
                    element
                    for element in elements
                    if element.is_displayed()
                ]

                return len(visible) == 0

            except StaleElementReferenceException:
                # DOM replacement itself is a valid indication that
                # the modal is being closed/re-rendered.
                return True

        try:

            WebDriverWait(
                self.driver,
                15,
                poll_frequency=0.2,
                ignored_exceptions=(
                    StaleElementReferenceException,
                )
            ).until(
                modal_closed
            )

            print(
                "Reassign modal closed after Submit"
            )

        except TimeoutException:

            # Do not click Submit a second time.
            # The API may still be processing or the UI may display
            # a confirmation/toast without immediately removing the modal.
            print(
                "Reassign modal is still visible after Submit; "
                "Submit click was already completed."
            )

        # =========================================================
        # STEP 7 - WAIT BEFORE REFRESHING THE LIST
        #
        # IMPORTANT:
        # The Reassign API may need a few seconds to update the
        # backend. Refreshing immediately can make the list temporarily
        # show the old Product/Variant or an intermediate state.
        #
        # This is intentionally the same pattern used for the QR
        # generation status transitions.
        # =========================================================

        print(
            "Waiting before refreshing QR list after Reassign..."
        )

        time.sleep(5)

        print(
            "Reassign wait completed. Safe to refresh list."
        )

        # =========================================================
        # STEP 8 - OPEN A FRESH QR LIST PAGE
        #
        # IMPORTANT:
        # Submit can succeed before the existing QR List table has
        # refreshed. The old Angular/DataTables row may therefore
        # still show the previous Product/Variant.
        #
        # Force a fresh list-page load before validating the result.
        # =========================================================

        print(
            "Reassign submitted. Starting backend/list synchronization..."
        )

        # wait_for_reassignment_update() performs the deliberate
        # backend-settling wait and ONE fresh QR Management page load.
        self.wait_for_reassignment_update(
            batch_no,
            new_product,
            new_variant,
            timeout=60
        )

        print(
            f"Reassign validation data is ready for batch: "
            f"{batch_no}"
        )

        return True

    def open_reassign_modal(self, batch_no):

        print(
            f"Opening Reassign for batch: {batch_no}"
        )

        # =====================================================
        # STEP 1 - LOCATOR FOR THE BATCH ROW
        # =====================================================

        row_locator = (
            By.XPATH,
            f"//table//tbody//tr[contains(., '{batch_no}')]"
        )

        action_locator = (
            By.XPATH,
            f"//table//tbody//tr[contains(., '{batch_no}')]"
            "//td[last()]//button"
        )

        # =====================================================
        # STEP 2 - MAKE SURE FRESH ROW EXISTS
        # =====================================================

        WebDriverWait(
            self.driver,
            30,
            poll_frequency=0.5,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.visibility_of_element_located(
                row_locator
            )
        )

        print(
            f"Fresh row found for Reassign: {batch_no}"
        )

        # =====================================================
        # STEP 3 - CLICK THREE DOTS
        #
        # IMPORTANT:
        # NEVER STORE THE BUTTON ELEMENT.
        # RE-FIND IT WHENEVER WE NEED IT.
        # =====================================================

        menu_opened = False

        for attempt in range(1, 6):

            try:

                print(
                    f"Clicking three-dot menu "
                    f"(attempt {attempt}/5)"
                )

                # Get a COMPLETELY FRESH button
                action_button = WebDriverWait(
                    self.driver,
                    10,
                    poll_frequency=0.3,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.element_to_be_clickable(
                        action_locator
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    action_button
                )

                # Small pause allows Angular table rendering
                time.sleep(0.3)

                # RE-FIND again because scroll/render can make
                # the previous element stale
                action_button = WebDriverWait(
                    self.driver,
                    5,
                    poll_frequency=0.2,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.element_to_be_clickable(
                        action_locator
                    )
                )

                action_button.click()

                # =================================================
                # STEP 4 - VERIFY MENU REALLY OPENED
                # =================================================

                WebDriverWait(
                    self.driver,
                    5,
                    poll_frequency=0.2,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//a[normalize-space()='Re-assign']"
                            " | "
                            "//button[normalize-space()='Re-assign']"
                        )
                    )
                )

                print(
                    "Three-dot menu verified OPEN"
                )

                menu_opened = True
                break

            except (
                    StaleElementReferenceException,
                    TimeoutException
            ):

                print(
                    f"Three-dot click attempt "
                    f"{attempt} failed - retrying"
                )

                time.sleep(0.5)

        if not menu_opened:
            raise AssertionError(
                f"Could not open three-dot menu "
                f"for batch: {batch_no}"
            )

        # =====================================================
        # STEP 5 - CLICK RE-ASSIGN
        #
        # AGAIN: DO NOT STORE THE ELEMENT.
        # FIND IT FRESH.
        # =====================================================

        reassign_locator = (
            By.XPATH,
            "//a[normalize-space()='Re-assign']"
            " | "
            "//button[normalize-space()='Re-assign']"
        )

        WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.3,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.visibility_of_element_located(
                reassign_locator
            )
        )

        print(
            "Clicking Re-assign"
        )

        reassign_clicked = False

        for attempt in range(1, 4):

            try:

                # ALWAYS FIND FRESH
                reassign_option = WebDriverWait(
                    self.driver,
                    5,
                    poll_frequency=0.2,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.element_to_be_clickable(
                        reassign_locator
                    )
                )

                reassign_option.click()

                reassign_clicked = True
                print(
                    "Re-assign clicked"
                )
                break

            except StaleElementReferenceException:

                print(
                    f"Re-assign element became stale "
                    f"(attempt {attempt}/3) - retrying"
                )

                time.sleep(0.5)

        if not reassign_clicked:
            raise AssertionError(
                f"Could not click Re-assign "
                f"for batch: {batch_no}"
            )

        # =====================================================
        # STEP 6 - VERIFY REASSIGN MODAL
        # =====================================================

        modal_locator = (
            By.XPATH,
            "//div[contains(@class,'modal')]"
            "[.//*[normalize-space()='Reassign QR']]"
        )

        WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.3,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.visibility_of_element_located(
                modal_locator
            )
        )

        # Also verify Product field exists inside modal
        WebDriverWait(
            self.driver,
            10,
            poll_frequency=0.3,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'modal')]"
                    "//label[normalize-space()='Product']"
                )
            )
        )

        print(
            "Reassign modal verified OPEN"
        )


    # =========================================================
    # BATCH RELOCATION / UPDATE LOCATION
    # =========================================================

    def open_action_menu(self, batch_no):
        """
        Open the three-dot Action menu for the requested batch.

        Always locate a fresh button because the QR table is
        re-rendered by Angular/DataTables.
        """

        action_locator = (
            By.XPATH,
            f"//table//tbody//tr[contains(., '{batch_no}')]"
            "//td[last()]//button"
        )

        menu_locator = (
            By.XPATH,
            "//ul[contains(@class,'dropdown-menu') "
            "and contains(@class,'show')]"
            "//*[self::a or self::button]"
        )

        print(
            f"Opening three-dot menu for batch: {batch_no}"
        )

        for attempt in range(1, 6):

            try:

                action_button = WebDriverWait(
                    self.driver,
                    10,
                    poll_frequency=0.2,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.element_to_be_clickable(
                        action_locator
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });
                    """,
                    action_button
                )

                time.sleep(0.3)

                # Re-find after scroll/render.
                action_button = WebDriverWait(
                    self.driver,
                    5,
                    poll_frequency=0.2,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.element_to_be_clickable(
                        action_locator
                    )
                )

                try:
                    action_button.click()

                except (
                    StaleElementReferenceException,
                    ElementClickInterceptedException,
                ):

                    action_button = WebDriverWait(
                        self.driver,
                        5,
                        poll_frequency=0.2,
                        ignored_exceptions=(
                            StaleElementReferenceException,
                        )
                    ).until(
                        EC.element_to_be_clickable(
                            action_locator
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        action_button
                    )

                WebDriverWait(
                    self.driver,
                    5,
                    poll_frequency=0.2,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.visibility_of_element_located(
                        menu_locator
                    )
                )

                print(
                    "Three-dot menu verified OPEN"
                )

                return True

            except (
                StaleElementReferenceException,
                TimeoutException,
                ElementClickInterceptedException,
            ):

                print(
                    f"Three-dot menu attempt "
                    f"{attempt}/5 failed - retrying"
                )

                time.sleep(0.5)

        raise AssertionError(
            f"Could not open three-dot menu "
            f"for batch: {batch_no}"
        )

    def click_action_option(self, option_text):
        """
        Click an option from the currently open three-dot menu.
        """

        option_locator = (
            By.XPATH,
            "//ul[contains(@class,'dropdown-menu') "
            "and contains(@class,'show')]"
            "//*[self::a or self::button]"
            f"[normalize-space()='{option_text}']"
        )

        print(
            f"Clicking Action menu option: {option_text}"
        )

        for attempt in range(1, 4):

            try:

                option = WebDriverWait(
                    self.driver,
                    10,
                    poll_frequency=0.2,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.element_to_be_clickable(
                        option_locator
                    )
                )

                try:
                    option.click()

                except (
                    StaleElementReferenceException,
                    ElementClickInterceptedException,
                ):

                    option = WebDriverWait(
                        self.driver,
                        5,
                        poll_frequency=0.2,
                        ignored_exceptions=(
                            StaleElementReferenceException,
                        )
                    ).until(
                        EC.element_to_be_clickable(
                            option_locator
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        option
                    )

                print(
                    f"{option_text} clicked"
                )

                return True

            except StaleElementReferenceException:

                print(
                    f"{option_text} became stale "
                    f"(attempt {attempt}/3)"
                )

                time.sleep(0.5)

        raise AssertionError(
            f"Could not click Action menu option: "
            f"{option_text}"
        )

    def open_update_location_modal(self, batch_no):
        """
        From the QR list:
            three dots -> Update Location

        Uses the actual Update Location menu item shown in the UI.
        """

        print(
            f"Opening Update Location for batch: {batch_no}"
        )

        self.wait_for_batch(batch_no)

        self.open_action_menu(batch_no)

        update_location_locator = (
            By.XPATH,
            "//ul[contains(@class,'dropdown-menu') "
            "and contains(@class,'show')]"
            "//button[contains(@class,'loc_update') "
            "and normalize-space()='Update Location']"
            " | "
            "//ul[contains(@class,'dropdown-menu') "
            "and contains(@class,'show')]"
            "//a[normalize-space()='Update Location']"
        )

        for attempt in range(1, 4):

            try:

                option = WebDriverWait(
                    self.driver,
                    10,
                    poll_frequency=0.2,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.element_to_be_clickable(
                        update_location_locator
                    )
                )

                try:
                    option.click()

                except (
                    StaleElementReferenceException,
                    ElementClickInterceptedException,
                ):

                    option = WebDriverWait(
                        self.driver,
                        5,
                        poll_frequency=0.2,
                        ignored_exceptions=(
                            StaleElementReferenceException,
                        )
                    ).until(
                        EC.element_to_be_clickable(
                            update_location_locator
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        option
                    )

                break

            except StaleElementReferenceException:

                print(
                    f"Update Location became stale "
                    f"(attempt {attempt}/3)"
                )

                time.sleep(0.5)

        modal_locator = (
            By.XPATH,
            "//div[@id='reassignLocation']"
            "[contains(@class,'show') or "
            "contains(@style,'display: block')]"
            " | "
            "//div[@id='reassignLocation']"
        )

        WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.visibility_of_element_located(
                modal_locator
            )
        )

        WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='reassignLocation']"
                    "//*[contains("
                    "normalize-space(),"
                    "'Select Batch Location'"
                    ")]"
                )
            )
        )

        print(
            "Update Batch Location modal verified OPEN"
        )

        return True

    def select_batch_location(self, location="Mumbai"):
        """
        Select2 flow from the supplied UI:

            Select Batch Location
                -> type Mumbai
                -> Mumbai, Maharashtra, India
        """

        location_dropdown_locator = (
            By.XPATH,
            "//div[@id='reassignLocation']"
            "//select[@name='batch_location']"
            "/following-sibling::span"
            "[contains(@class,'select2-container')]"
            "//span[contains("
            "@class,"
            "'select2-selection--single'"
            ")]"
            " | "
            "//div[@id='reassignLocation']"
            "//select[@name='batch_location']"
            "/following::span[contains("
            "@class,"
            "'select2-selection--single'"
            ")][1]"
        )

        open_locator = (
            By.XPATH,
            "//span[contains("
            "@class,"
            "'select2-container--open'"
            ")]"
        )

        search_locator = (
            By.XPATH,
            "//span[contains("
            "@class,"
            "'select2-container--open'"
            ")]"
            "//input[contains("
            "@class,"
            "'select2-search__field'"
            ")]"
        )

        option_locator = (
            By.XPATH,
            "//span[contains("
            "@class,"
            "'select2-container--open'"
            ")]"
            "//li[@role='option'"
            " and not(contains("
            "@class,"
            "'select2-results__message'"
            "))]"
            "[normalize-space()='Mumbai, Maharashtra, India']"
        )

        selected_locator = (
            By.XPATH,
            "//div[@id='reassignLocation']"
            "//span[contains("
            "@class,"
            "'select2-selection__rendered'"
            ")]"
            "[normalize-space()='Mumbai, Maharashtra, India']"
        )

        def find_dropdown(driver):
            try:

                elements = driver.find_elements(
                    *location_dropdown_locator
                )

                for element in elements:

                    try:
                        if element.is_displayed():
                            return element

                    except StaleElementReferenceException:
                        continue

            except StaleElementReferenceException:
                return False

            return False

        print(
            "Locating Select Batch Location dropdown..."
        )

        dropdown = WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            find_dropdown
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center'
            });
            """,
            dropdown
        )

        dropdown = WebDriverWait(
            self.driver,
            10,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            find_dropdown
        )

        print(
            "Clicking Select Batch Location dropdown"
        )

        try:

            ActionChains(
                self.driver
            ).move_to_element(
                dropdown
            ).click().perform()

        except (
            StaleElementReferenceException,
            ElementClickInterceptedException,
        ):

            dropdown = WebDriverWait(
                self.driver,
                10,
                poll_frequency=0.2,
                ignored_exceptions=(
                    StaleElementReferenceException,
                )
            ).until(
                find_dropdown
            )

            self.driver.execute_script(
                "arguments[0].click();",
                dropdown
            )

        WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.visibility_of_element_located(
                open_locator
            )
        )

        print(
            "Batch Location dropdown OPENED"
        )

        search_box = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.visibility_of_element_located(
                search_locator
            )
        )

        search_box.click()
        search_box.clear()
        search_box.send_keys(location)

        print(
            f"Typed {location} into Batch Location search"
        )

        WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.visibility_of_element_located(
                option_locator
            )
        )

        print(
            "Mumbai, Maharashtra, India option displayed"
        )

        for attempt in range(1, 4):

            try:

                option = WebDriverWait(
                    self.driver,
                    10,
                    poll_frequency=0.2,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                    )
                ).until(
                    EC.element_to_be_clickable(
                        option_locator
                    )
                )

                try:
                    option.click()

                except (
                    StaleElementReferenceException,
                    ElementClickInterceptedException,
                ):

                    option = WebDriverWait(
                        self.driver,
                        5,
                        poll_frequency=0.2,
                        ignored_exceptions=(
                            StaleElementReferenceException,
                        )
                    ).until(
                        EC.element_to_be_clickable(
                            option_locator
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        option
                    )

                break

            except StaleElementReferenceException:

                print(
                    f"Mumbai option became stale "
                    f"(attempt {attempt}/3)"
                )

                time.sleep(0.5)

        WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.visibility_of_element_located(
                selected_locator
            )
        )

        print(
            "Selected Batch Location verified: "
            "Mumbai, Maharashtra, India"
        )

        return "Mumbai, Maharashtra, India"

    def submit_location_update(self, batch_no=None):
        """
        Submit Update Batch Location.

        The batch number is accepted for consistent test logging,
        but the modal itself contains the actual Submit button.
        """

        submit_locator = (
            By.XPATH,
            "//div[@id='reassignLocation']"
            "//div[contains(@class,'modal-footer')]"
            "//button[normalize-space()='Submit']"
        )

        submit_button = WebDriverWait(
            self.driver,
            15,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.element_to_be_clickable(
                submit_locator
            )
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            submit_button
        )

        # Re-find after scroll.
        submit_button = WebDriverWait(
            self.driver,
            10,
            poll_frequency=0.2,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        ).until(
            EC.element_to_be_clickable(
                submit_locator
            )
        )

        print(
            f"Clicking Submit for Batch Location"
            + (f": {batch_no}" if batch_no else "")
        )

        try:
            submit_button.click()

        except (
            StaleElementReferenceException,
            ElementClickInterceptedException,
        ):

            submit_button = WebDriverWait(
                self.driver,
                10,
                poll_frequency=0.2,
                ignored_exceptions=(
                    StaleElementReferenceException,
                )
            ).until(
                EC.element_to_be_clickable(
                    submit_locator
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                submit_button
            )

        print(
            "Batch Location Submit clicked"
        )

        modal_locator = (
            By.ID,
            "reassignLocation"
        )

        def modal_closed(driver):
            try:

                elements = driver.find_elements(
                    *modal_locator
                )

                return not any(
                    element.is_displayed()
                    for element in elements
                )

            except StaleElementReferenceException:
                return True

        try:

            WebDriverWait(
                self.driver,
                20,
                poll_frequency=0.2,
                ignored_exceptions=(
                    StaleElementReferenceException,
                )
            ).until(
                modal_closed
            )

            print(
                "Update Batch Location modal closed"
            )

        except TimeoutException:

            print(
                "Update Batch Location modal is still visible; "
                "Submit was already clicked."
            )

        return True

    def wait_for_location_update(
            self,
            batch_no,
            expected_location="Mumbai, Maharashtra, India",
            timeout=60
    ):
        """
        Synchronization wait after Update Location Submit.

        Location update has the same frontend/backend timing pattern
        seen in QR status transitions and Reassign.

        Do not immediately reload the list after Submit. Give the
        backend/API time to persist the new location first.
        """

        print("=" * 60)
        print(
            f"WAITING FOR LOCATION UPDATE : [{batch_no}]"
        )
        print(
            f"Expected Location : {expected_location}"
        )
        print("=" * 60)

        start = time.time()

        # Same deliberate initial wait pattern used by the working
        # Reassign implementation.
        print(
            "Waiting for Batch Location backend processing..."
        )

        time.sleep(5)

        elapsed = time.time() - start

        if elapsed > timeout:
            raise AssertionError(
                "Location update synchronization exceeded "
                f"{timeout} seconds."
            )

        print(
            "Location update backend wait completed"
        )

        return True

    def wait_for_batch_view_page(self, timeout=30):
        """
        Synchronize after clicking View.

        The View page is already loaded when the URL changes to /show.
        Do not depend on a particular Bootstrap/container structure.

        We only wait for:
            - the /show URL
            - the visible text "Batch Location"
        """

        wait = WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=0.25,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        )

        # Wait until navigation to the View page is complete.
        wait.until(
            lambda d:
            "/admin/qr-management/" in d.current_url
            and "/show" in d.current_url
        )

        print(
            f"QR Batch View URL loaded: {self.driver.current_url}"
        )

        # The application renders the label with spacing/newlines
        # depending on the DOM. Match the text content, not a class.
        wait.until(
            lambda d: any(
                el.is_displayed()
                for el in d.find_elements(
                    By.XPATH,
                    "//*[contains(normalize-space(.), "
                    "'Batch Location')]"
                )
            )
        )

        print(
            "Batch Location label rendered on View page"
        )

        return True

    def get_batch_location_from_view(self):
        wait = WebDriverWait(self.driver, 30)

        def read_batch_location(driver):
            try:
                location_element = driver.find_element(
                    By.XPATH,
                    "//div[contains(@class,'user_basic_details_title')"
                    " and contains(normalize-space(.),'Batch Location')]"
                    "/following-sibling::div[contains(@class,'req_details')]"
                    "//span"
                )

                value = location_element.get_attribute("textContent").strip()

                if value:
                    print(
                        f"Batch Location from View: {value}"
                    )
                    return value

            except Exception:
                return False

            return False

        return wait.until(read_batch_location)

    def _is_stale(self, element):

        try:
            element.is_enabled()
            return False

        except StaleElementReferenceException:
            return True