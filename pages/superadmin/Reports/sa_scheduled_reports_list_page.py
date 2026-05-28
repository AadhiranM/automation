from datetime import date, timedelta
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker
from selenium.webdriver.common.action_chains import ActionChains



class SAScheduledReportsPage(BasePage):

    # ======================================================
    # SEARCH
    # ======================================================
    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    # ======================================================
    # FILTERS
    # ======================================================
    DATE_FILTER = (
        By.ID,
        "datepicker-range"
    )

    STATUS_DROPDOWN = (
        By.ID,
        "select2-idStatus-container"
    )

    # ======================================================
    # TABLE
    # ======================================================
    FIRST_ROW = (
        By.XPATH,
        "//table/tbody/tr[1]"
    )

    NO_DATA = (
        By.XPATH,
        "//td[contains(@class,'dataTables_empty')]"
    )

    FIRST_PRODUCT = (
        By.XPATH,
        "//table/tbody/tr[1]/td[6]"
    )

    FIRST_COMMENT = (
        By.XPATH,
        "//table/tbody/tr[1]/td[last()]"
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

    FIRST_SCAN_ID = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    PREVIOUS_BTN = (
        By.XPATH,
        "//a[normalize-space()='Previous']"
    )
    PAGE_NUMBER = "//a[normalize-space()='{}']"

    # ======================================================
    # EDIT PAGE
    # ======================================================


    SUBMIT_BTN = (
         By.XPATH,
         "//button[contains(text(),'Submit')]"
    )

    SUCCESS_MSG = (
        By.XPATH,
        "//*[contains(text(),'successfully')]"
    )
    # ======================================================
    # EXPORT
    # ======================================================

    CREATE_BTN = (
        By.XPATH,
        "//button[contains(.,'Create')]"
    )


    DEACTIVATE_BTN = (
        By.XPATH,
        "//a[contains(.,'Deactivate')]"
    )

    ACTIVATE_BTN = (
        By.XPATH,
        "//a[contains(.,'Activate')]"
    )

    CONFIRM_BTN = (
        By.XPATH,
        "//button[contains(.,'Deactivate') or contains(.,'Activate')]"
    )

    OK_BTN = (
        By.XPATH,
        "//button[contains(.,'OK')]"
    )

    ACTIONS_BTN = (
        By.XPATH,
        "//table[@id='crudTable']/tbody/tr[1]/td[last()]//button[contains(@class,'dropdown')]"
    )

    EDIT_BTN = (
        By.XPATH,
        "//ul[contains(@class,'dropdown-menu') and contains(@class,'show')]//button[contains(@class,'edit-report-btn')]"
    )

    TOGGLE_BTN = (
        By.XPATH,
        "//ul[contains(@class,'dropdown-menu') and contains(@class,'show')]//button[contains(@class,'toggle-status-btn')]"
    )



    MAIL_TIME_DROPDOWN = (
        By.ID,
        "select2-mail_send_at-container"
    )

    CONFIRM_DEACTIVATE_BTN = (
        By.XPATH,
        "//button[contains(text(),'Deactivate')]"
    )
    FIRST_ROW_STATUS = (
        By.XPATH,
        "//table[@id='crudTable']/tbody/tr[1]//span[contains(text(),'Active') or contains(text(),'Inactive')]"
    )

    FIRST_ROW_MAIL_TIME = (
        By.XPATH,
        "//table[@id='crudTable']/tbody/tr[1]/td[8]"
    )

    UPDATE_BTN = (
        By.XPATH,
        "//button[contains(text(),'Update')]"
    )

    def click_create(self):
        wait = WebDriverWait(self.driver, 30)

        wait.until(
            EC.element_to_be_clickable(self.CREATE_BTN)
        ).click()

        time.sleep(3)
    def goto_page(self):
        self.driver.get(
            "https://beta.digitathya.com/admin/auto-generate-report?reset_filters=1"
        )
        self.wait_for_results()
    # ======================================================
    # WAIT
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

    def search_first_record(self):
        scan_id = self.get_text(
            self.FIRST_SCAN_ID
        ).strip()

        self.type(self.SEARCH_BOX, scan_id)
        self.click(self.SEARCH_BTN)

        self.wait_for_results()

        return scan_id
    # ======================================================
    # STATUS FILTER
    # ======================================================

    def filter_by_status(self, status):
        wait = WebDriverWait(self.driver, 30)

        print(f"Selecting status = {status}")

        # exact visible status dropdown
        dropdown = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//span[@id='select2-idStatus-container']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )
        time.sleep(2)

        # ActionChains click (stronger than normal click)
        ActionChains(self.driver).move_to_element(dropdown).click().perform()

        print("Status dropdown clicked")
        time.sleep(2)

        # select option from opened dropdown
        option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//li[@role='option' and normalize-space()='{status}']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'nearest'});",
            option
        )
        time.sleep(1)

        ActionChains(self.driver).move_to_element(option).click().perform()

        print(f"Selected status = {status}")

        time.sleep(3)

        rows = self.driver.find_elements(
            By.XPATH,
            "//table/tbody/tr"
        )

        no_data = self.driver.find_elements(
            By.XPATH,
            "//*[contains(text(),'No data available')]"
        )

        assert len(rows) > 0 or len(no_data) > 0
    # ======================================================
    # DATE FILTER
    # ======================================================

    def filter_date(self, start, end):

        self.click(self.DATE_FILTER)

        picker = FlatpickrRangePicker(self.driver)

        picker.select_range(start, end)

        self.wait_for_results()
    # ======================================================
    # ENTRIES
    # ======================================================

    def set_entries_per_page(self, value):

        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                self.ENTRIES_DROPDOWN
            )
        )

        Select(dropdown).select_by_value(str(value))

        self.wait_for_results()
    # ======================================================
    # PAGINATION
    # ======================================================

    def click_next(self):

        next_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.NEXT_BTN)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            next_btn
        )

        self.wait_for_results()

    def click_previous(self):

        prev_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PREVIOUS_BTN)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            prev_btn
        )

        self.wait_for_results()

    def go_to_page(self, number):

        page = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                self.PAGE_NUMBER.format(number)
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            page
        )

        self.wait_for_results()
    # ======================================================
    # VIEW
    # ======================================================


    def is_row_present(self):

        return len(
            self.driver.find_elements(*self.FIRST_ROW)
        ) > 0

    def has_no_data(self):

        return len(
            self.driver.find_elements(*self.NO_DATA)
        ) > 0


    def get_first_row_status(self):
        return self.get_text(self.FIRST_ROW_STATUS).strip()

    def get_first_row_mail_time(self):
        return self.get_text(self.FIRST_ROW_MAIL_TIME).strip()

    def open_first_row_actions(self):
        wait = WebDriverWait(self.driver, 20)

        action_btn = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//table/tbody/tr[1]//td[last()]//button | //table/tbody/tr[1]//td[last()]//*[contains(@class,'dropdown-toggle')] | //table/tbody/tr[1]//td[last()]//*[contains(text(),'...')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            action_btn
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            action_btn
        )

        time.sleep(2)

    import random

    def edit_first_schedule_report(self):
        wait = WebDriverWait(self.driver, 30)

        self.open_first_row_actions()

        edit_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@class,'edit-report-btn')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            edit_btn
        )

        print("Edit clicked")

        wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//h5[contains(text(),'Edit Schedule Report')]"
            ))
        )

        update_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(text(),'Update')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            update_btn
        )

        print("Update clicked")

        wait.until(
            EC.invisibility_of_element_located((
                By.XPATH,
                "//h5[contains(text(),'Edit Schedule Report')]"
            ))
        )

        return True

    def deactivate_first_schedule_report(self):
        self.open_first_row_actions()

        self.safe_click(self.DEACTIVATE_BTN)

        self.safe_click(self.CONFIRM_BTN)

        self.safe_click(self.OK_BTN)

        time.sleep(2)

        return self.get_first_row_status()

    def activate_first_schedule_report(self):
        self.open_first_row_actions()

        self.safe_click(self.ACTIVATE_BTN)

        self.safe_click(self.CONFIRM_BTN)

        self.safe_click(self.OK_BTN)

        time.sleep(2)

        return self.get_first_row_status()

    def toggle_first_schedule_report_status(self):
        wait = WebDriverWait(self.driver, 30)

        current_status = self.get_text(
            self.FIRST_ROW_STATUS
        ).strip()

        print("CURRENT STATUS =", current_status)

        # open 3 dots
        actions = wait.until(
            EC.element_to_be_clickable(self.ACTIONS_BTN)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            actions
        )

        time.sleep(1)

        # click action based on current status
        if current_status == "Active":
            action_btn = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[normalize-space()='Deactivate']"
                ))
            )
            expected = "Inactive"

        else:
            action_btn = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[normalize-space()='Activate']"
                ))
            )
            expected = "Active"

        self.driver.execute_script(
            "arguments[0].click();",
            action_btn
        )

        print("Dropdown action clicked")

        time.sleep(2)

        # popup confirm button
        confirm_btn = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class,'swal2-popup')]//button[contains(@class,'swal2-confirm')]"
            ))
        )

        ActionChains(self.driver).move_to_element(confirm_btn).click().perform()

        print("Popup confirm clicked")

        time.sleep(3)

        # success popup OK button (if appears)
        try:
            ok_btn = WebDriverWait(self.driver, 8).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[normalize-space()='OK']"
                ))
            )

            self.driver.execute_script(
                "arguments[0].click();",
                ok_btn
            )

            print("Success OK clicked")

        except:
            print("No OK popup appeared")

        time.sleep(3)

        new_status = self.get_text(
            self.FIRST_ROW_STATUS
        ).strip()

        print("NEW STATUS =", new_status)

        return current_status, new_status