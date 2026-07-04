import random
import time
from datetime import timedelta, date

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker
from selenium.webdriver.common.keys import Keys


class SAQRMonitoringPage(BasePage):

    # ======================================================
    # SEARCH
    # ======================================================
    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    # ======================================================
    # DATE FILTER
    # ======================================================
    DATE_FILTER = (By.ID, "datepicker-range")

    # ======================================================
    # STATUS FILTER
    # ======================================================
    STATUS_DROPDOWN = (By.ID, "select2-idStatus-container")

    # ======================================================
    # TABLE
    # ======================================================
    FIRST_ROW = (By.XPATH, "//table/tbody/tr[1]")

    NO_DATA = (
        By.XPATH,
        "//td[contains(@class,'dataTables_empty')]"
    )

    SCAN_IDS = (
        By.XPATH,
        "//table/tbody/tr/td[1]"
    )

    # ======================================================
    # ENTRIES
    # ======================================================
    ENTRIES_DROPDOWN = (
        By.NAME,
        "crudTable_length"
    )

    # ======================================================
    # PAGINATION
    # ======================================================
    NEXT_BTN = (
        By.XPATH,
        "//a[normalize-space()='Next']"
    )

    PREVIOUS_BTN = (
        By.XPATH,
        "//a[normalize-space()='Previous']"
    )

    PAGE_NUMBER = "//a[normalize-space()='{}']"

    # ======================================================
    # EXPORT
    # ======================================================
    EXPORT_BTN = (
        By.XPATH,
        "//button[contains(.,'Export')]"
    )

    START_ID = (By.ID, "fromId")

    END_ID = (By.ID, "toId")

    ID_BASED_TAB = (By.ID, "id-tab")

    EXPORT_POPUP = (By.ID, "modeSelectionModal")

    EXPORT_SUBMIT = (
        By.XPATH,
        "//div[@id='modeSelectionModal']//button[@type='submit']"
    )

    GO_TO_REPORTS = (
        By.XPATH,
        "//a[contains(.,'Go to Reports Page')]"
    )

    REPORT_TABLE = (
        By.XPATH,
        "//table"
    )

    USER_BASED_TAB = (By.ID, "user-tab")
    USER_DROPDOWN = (
        By.ID,
        "export-user-select"
    )

    USER_SEARCH = (
        By.XPATH,
        "//input[@name='search_terms']"
    )

    USER_SELECT = (
        By.XPATH,
        "//div[@id='userTabPane']//div[contains(@class,'choices__inner')]"
    )

    USER_SEARCH_BOX = (
        By.XPATH,
        "//div[@id='userTabPane']//input[contains(@class,'choices__input')]"
    )

    DATE_RANGE = (
        By.XPATH,
        "//input[contains(@placeholder,'Select Date')]"
    )

    DATE_BASED_TAB = (By.ID, "date-tab")
    DATE_BASED_RANGE = (
        By.XPATH,
        "//div[@id='dateTabPane']//input[contains(@placeholder,'Select Date Range')]"
    )
    START_TIME = (By.ID, "start_time")
    END_TIME = (By.ID, "end_time")



    EXPORT_SUCCESS = (
        By.XPATH,
        "//h4[contains(.,'Report Export Queued')]"
    )

    SCAN_ID_FIRST = (
        By.XPATH,
        "//table/tbody/tr[1]/td[1]"
    )

    SCAN_ID_SECOND = (
        By.XPATH,
        "//table/tbody/tr[2]/td[1]"
    )

    FIRST_ROW_USER = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    LATEST_DOWNLOAD_BTN = (
        By.XPATH,
        "(//table/tbody/tr[1]//a | //table/tbody/tr[1]//button)[last()]"
    )

    ROW1_USER = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    ROW2_USER = (
        By.XPATH,
        "//table/tbody/tr[2]/td[2]"
    )

    # ======================================================
    # NAVIGATION
    # ======================================================
    def goto_page(self):
        self.driver.get(
            "https://beta.digitathya.com/admin/qr-code-monitoring?reset_filters=1"
        )
        self.wait_for_results()

    # ======================================================
    # COMMON WAIT
    # ======================================================
    def wait_for_results(self):
        WebDriverWait(self.driver, 15).until(
            lambda d:
            d.find_elements(*self.FIRST_ROW)
            or
            d.find_elements(*self.NO_DATA)
        )

    # ======================================================
    # SEARCH
    # ======================================================
    def search(self, value):
        rows = self.driver.find_elements(*self.SCAN_IDS)

        if rows:
            value = rows[0].text.strip()

        self.type(self.SEARCH_BOX, value)
        self.click(self.SEARCH_BTN)
        self.wait_for_results()

    # ======================================================
    # STATUS FILTER
    # ======================================================
    def filter_by_status(self, status):
        self.click(self.STATUS_DROPDOWN)

        option = (
            By.XPATH,
            f"//li[contains(@class,'select2-results__option')]//span[normalize-space()='{status}']"
        )

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(option)
        )

        self.click(option)
        self.wait_for_results()

    # ======================================================
    # DATE FILTER
    # ======================================================
    def filter_date(self, start, end):

        self.safe_click(self.DATE_FILTER)

        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(start, end)

        self.click(self.SEARCH_BTN)

        self.wait_for_results()
    # ======================================================
    # ENTRIES
    # ======================================================
    def set_entries_per_page(self, value):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.ENTRIES_DROPDOWN)
        )

        Select(dropdown).select_by_value(str(value))
        self.wait_for_results()

    # ======================================================
    # PAGINATION
    # ======================================================
    def click_next(self):

        wait = WebDriverWait(self.driver, 10)

        next_btn = wait.until(
            EC.presence_of_element_located(self.NEXT_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            next_btn
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            next_btn
        )

        print("Next button clicked")

    def click_previous(self):
        prev_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PREVIOUS_BTN)
        )

        self.driver.execute_script("arguments[0].click();", prev_btn)
        self.wait_for_results()

    def go_to_page(self, number):
        page = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.PAGE_NUMBER.format(number))
            )
        )

        self.driver.execute_script("arguments[0].click();", page)
        self.wait_for_results()

    # ======================================================
    # EXPORT
    # ======================================================
    def click_export(self):
        self.click(self.EXPORT_BTN)

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.EXPORT_POPUP)
        )

    def go_to_reports_page(self):
        self.click(self.GO_TO_REPORTS)

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.REPORT_TABLE)
        )

    def export_id_based(self):

        wait = WebDriverWait(self.driver, 30)

        # ======================================
        # GET IDS FROM LIST
        # ======================================

        start_id = wait.until(
            EC.visibility_of_element_located(
                self.SCAN_ID_SECOND
            )
        ).text.strip()

        end_id = wait.until(
            EC.visibility_of_element_located(
                self.SCAN_ID_FIRST
            )
        ).text.strip()

        print(f"Start ID : {start_id}")
        print(f"End ID   : {end_id}")

        rows = self.driver.find_elements(
            By.XPATH,
            "//table/tbody/tr"
        )

        users = []

        for row in rows:

            scan_id = row.find_element(
                By.XPATH,
                "./td[1]"
            ).text.strip()

            if scan_id in [start_id, end_id]:

                user_text = row.find_element(
                    By.XPATH,
                    "./td[2]"
                ).text.strip()

                username = user_text.split("\n")[0].strip()

                if username and username not in users:
                    users.append(username)

        print("Users :", users)

        # ======================================
        # OPEN EXPORT POPUP
        # ======================================

        export_btn = wait.until(
            EC.element_to_be_clickable(
                self.EXPORT_BTN
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            export_btn
        )

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "modeSelectionModal")
            )
        )

        print("Export popup opened")

        # ======================================
        # CLICK ID TAB
        # ======================================

        id_tab = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "id-tab")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            id_tab
        )

        print("ID tab clicked")

        # ======================================
        # START ID
        # ======================================

        start_box = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "fromId")
            )
        )

        start_box.clear()
        start_box.send_keys(start_id)

        print("Start entered")

        # ======================================
        # END ID
        # ======================================

        end_box = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "toId")
            )
        )

        end_box.clear()
        end_box.send_keys(end_id)

        print("End entered")

        # ==========================================
        # ======================================
        # SELECT USERS FROM LIST
        # ======================================

        for username in users:
            self.select_export_user(username)

        print("All users selected")
        # ==========================
        # SUBMIT
        # ==========================

        submit_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(.,'Submit')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            submit_btn
        )

        print("Export Submitted")



    # ======================================================
    # VALIDATIONS
    # ======================================================
    def is_row_present(self):
        return len(self.driver.find_elements(*self.FIRST_ROW)) > 0

    def has_no_data(self):
        return len(self.driver.find_elements(*self.NO_DATA)) > 0

    def export_bulk_id_based(self):
        wait = WebDriverWait(self.driver, 20)

        scan_ids = self.driver.find_elements(
            By.XPATH,
            "//table//tbody/tr/td[1]"
        )

        ids = [scan_ids[i].text.strip() for i in range(min(3, len(scan_ids)))]
        bulk_ids = ",".join(ids)

        self.click(self.EXPORT_BTN)
        self.click((By.ID, "bulk-tab"))

        bulk_box = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//textarea[contains(@placeholder,'Enter scan ID')]"
            ))
        )

        bulk_box.clear()
        bulk_box.send_keys(bulk_ids)

        self.click(self.EXPORT_SUBMIT)

    def export_date_based(self):
        wait = WebDriverWait(self.driver, 20)

        self.click(self.EXPORT_BTN)

        wait.until(
            EC.visibility_of_element_located(self.EXPORT_POPUP)
        )

        self.click(self.DATE_BASED_TAB)

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "dateTabPane")
            )
        )

        date_input = wait.until(
            EC.element_to_be_clickable(self.DATE_BASED_RANGE)
        )
        date_input.click()

        time.sleep(1)

        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(
            date.today() - timedelta(days=7),
            date.today()
        )

        self.click(self.EXPORT_SUBMIT)

        wait.until(
            EC.visibility_of_element_located(self.EXPORT_SUCCESS)
        )

    def export_user_based(self):

        wait = WebDriverWait(self.driver, 30)

        # ======================================
        # GET FIRST USER FROM GRID
        # ======================================

        first_user_text = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//table/tbody/tr[1]/td[2]"
            ))
        ).text.strip()

        username = first_user_text.split("\n")[0].strip()

        print(f"First User : {username}")

        # ======================================
        # EXPORT POPUP
        # ======================================

        wait.until(
            EC.visibility_of_element_located(
                self.EXPORT_POPUP
            )
        )

        # ======================================
        # USER BASED TAB
        # ======================================

        self.click(self.USER_BASED_TAB)

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "userTabPane")
            )
        )

        print("User tab clicked")

        # ======================================
        # SELECT USER
        # ======================================

        # ======================================
        # OPEN USER DROPDOWN
        # ======================================

        # ======================================
        # SELECT USER
        # ======================================

        self.select_export_user_user_tab(username)

        # ======================================
        # DATE RANGE
        # ======================================

        date_input = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[@id='userTabPane']//input[contains(@placeholder,'Select Date Range')]"
            ))
        )

        date_input.click()

        time.sleep(1)

        picker = FlatpickrRangePicker(
            self.driver
        )

        picker.select_range(
            date.today() - timedelta(days=7),
            date.today()
        )

        print("Date range selected")

        # ======================================
        # START TIME = 00:00:00
        # ======================================

        start_time = wait.until(
            EC.element_to_be_clickable(
                self.START_TIME
            )
        )

        start_time.click()

        active = self.driver.switch_to.active_element

        active.send_keys(Keys.ARROW_DOWN)
        active.send_keys(Keys.ENTER)

        print("Start time selected")

        # ======================================
        # END TIME = 00:00:00
        # ======================================

        end_time = wait.until(
            EC.element_to_be_clickable(
                self.END_TIME
            )
        )

        end_time.click()

        active = self.driver.switch_to.active_element

        active.send_keys(Keys.ARROW_DOWN)
        active.send_keys(Keys.ENTER)

        print("End time selected")

        # ======================================
        # SUBMIT
        # ======================================

        self.click(self.EXPORT_SUBMIT)

        wait.until(
            EC.visibility_of_element_located(
                self.EXPORT_SUCCESS
            )
        )

        print("Export Submitted")

    def select_export_user(self, username):

        wait = WebDriverWait(self.driver, 20)

        print(f"Searching User : {username}")

        # OPEN DROPDOWN

        dropdown = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class,'choices__inner')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            dropdown
        )


        time.sleep(2)

        # SEARCH BOX

        from selenium.webdriver.common.keys import Keys

        search_box = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//input[contains(@class,'choices__input')]"
            ))
        )

        search_box.clear()
        search_box.send_keys(username)

        print(f"Searching User : {username}")

        time.sleep(2)

        search_box.send_keys(Keys.ENTER)

        print(f"Selected User : {username}")

        time.sleep(2)

        # CLOSE ONLY DROPDOWN

        end_box = wait.until(
            EC.element_to_be_clickable((
                By.ID,
                "toId"
            ))

        )

        self.driver.execute_script(
            "arguments[0].click();",
            end_box
        )

        time.sleep(1)

        print("Dropdown closed")

    def select_export_user_user_tab(self, username):

        wait = WebDriverWait(self.driver, 20)

        print(f"Searching User : {username}")

        dropdown = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[@id='userTabPane']//div[contains(@class,'choices__inner')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            dropdown
        )

        time.sleep(2)

        search_box = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[@id='userTabPane']//input[contains(@class,'choices__input')]"
            ))
        )

        search_box.clear()
        search_box.send_keys(username)

        wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                f"//div[@id='userTabPane']//*[contains(text(),'{username}')]"
            ))
        )

        search_box.send_keys(Keys.ENTER)

        print(f"Selected User : {username}")

        time.sleep(2)

        # close dropdown only
        date_field = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//input[contains(@placeholder,'Select Date Range')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            date_field
        )

        time.sleep(1)

        print("Dropdown closed")