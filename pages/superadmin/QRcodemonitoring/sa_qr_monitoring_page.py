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

    EXPORT_POPUP = (
        By.XPATH,
        "//h5[contains(.,'Choose Export Criteria')]"
    )

    ID_BASED_TAB = (By.ID, "id-tab")

    START_ID = (
        By.XPATH,
        "//input[@placeholder='Enter Report Start ID']"
    )

    END_ID = (
        By.XPATH,
        "//input[@placeholder='Enter Report End ID']"
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
        "//input[contains(@placeholder,'Select Date Range')]"
    )

    DATE_BASED_TAB = (By.ID, "date-tab")
    DATE_BASED_RANGE = (
        By.XPATH,
        "//div[@id='dateTabPane']//input[contains(@placeholder,'Select Date Range')]"
    )
    START_TIME = (By.ID, "start_time")
    END_TIME = (By.ID, "end_time")

    EXPORT_SUBMIT = (
        By.XPATH,
        "//button[contains(.,'Submit')]"
    )

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
        self.click(self.DATE_FILTER)

        picker = FlatpickrRangePicker(self.driver)
        success = picker.select_range(start, end)

        if not success:
            raise Exception("Date range selection failed")

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
        next_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.NEXT_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            next_btn
        )

        next_btn.click()
        self.wait_for_results()

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

        wait = WebDriverWait(self.driver, 20)

        # ==========================================
        # GET IDS FROM TABLE
        # ==========================================

        start_id = self.get_text(self.SCAN_ID_SECOND).strip()
        end_id = self.get_text(self.SCAN_ID_FIRST).strip()

        print("Start ID :", start_id)
        print("End ID   :", end_id)

        # ==========================================
        # OPEN EXPORT POPUP
        # ==========================================

        export_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Export')]")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            export_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            export_btn
        )

        print("Export button clicked")

        # ==========================================
        # WAIT FOR POPUP
        # ==========================================

        wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//h5[contains(.,'Choose Export Criteria')] | //h4[contains(.,'Choose Export Criteria')]"
                )
            )
        )

        print("Export popup opened")

        # ==========================================
        # CLICK ID TAB
        # ==========================================

        id_tab = wait.until(
            EC.element_to_be_clickable(self.ID_BASED_TAB)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            id_tab
        )

        print("ID tab clicked")

        time.sleep(2)

        # ==========================================
        # USER DROPDOWN
        # ==========================================

        # ==========================================
        # USER DROPDOWN
        # ==========================================

        dropdown = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[contains(text(),'Select Users')]/following::div[contains(@class,'choices__inner')][1]"
            ))
        )

        dropdown.click()

        time.sleep(2)

        first_option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "(//div[contains(@class,'choices__list--dropdown')]//div[@role='option'])[1]"
            ))
        )

        selected_user = first_option.text.strip()

        print(f"Selected User : {selected_user}")

        self.driver.execute_script(
            "arguments[0].click();",
            first_option
        )

        time.sleep(2)

        # CLOSE DROPDOWN USING ESC
        from selenium.webdriver.common.keys import Keys



        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

        time.sleep(1)

        self.driver.execute_script("""
        document.querySelector('.modal-body').click();
        """)

        time.sleep(1)

        time.sleep(2)

        # ==========================================
        # START ID
        # ==========================================

        # ==========================================
        # START ID
        # ==========================================

        start_box = wait.until(
            EC.presence_of_element_located(self.START_ID)
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1];",
            start_box,
            start_id
        )

        self.driver.execute_script("""
        arguments[0].dispatchEvent(new Event('input',{bubbles:true}));
        arguments[0].dispatchEvent(new Event('change',{bubbles:true}));
        """, start_box)

        # ==========================================
        # END ID
        # ==========================================

        end_box = wait.until(
            EC.presence_of_element_located(self.END_ID)
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1];",
            end_box,
            end_id
        )

        self.driver.execute_script("""
        arguments[0].dispatchEvent(new Event('input',{bubbles:true}));
        arguments[0].dispatchEvent(new Event('change',{bubbles:true}));
        """, end_box)

        time.sleep(1)

        actual_start = start_box.get_attribute("value").strip()
        actual_end = end_box.get_attribute("value").strip()

        print("Actual Start :", actual_start)
        print("Actual End   :", actual_end)

        assert actual_start != "", "Start ID blank"
        assert actual_end != "", "End ID blank"

        # ==========================================
        # SUBMIT
        # ==========================================
        buttons = self.driver.find_elements(
            By.XPATH,
            "//button"
        )

        for btn in buttons:
            print("BUTTON =>", btn.text)

        submit_btn = wait.until(
            EC.element_to_be_clickable(self.EXPORT_SUBMIT)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            submit_btn
        )

        print("Export Submitted")
    # ======================================================
    # USER BASED EXPORT FIXED
    # ======================================================
    def export_user_based(self):
        wait = WebDriverWait(self.driver, 20)

        self.click(self.USER_BASED_TAB)

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "userTabPane")
            )
        )

        # open dropdown
        dropdown = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[@id='userTabPane']//div[contains(@class,'choices__inner')]"
            ))
        )
        dropdown.click()

        # search box
        search_box = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[@id='userTabPane']//input[contains(@class,'choices__input')]"
            ))
        )

        search_box.clear()
        search_box.send_keys("T")

        # wait options
        wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[@id='userTabPane']//div[contains(@class,'choices__item--choice')]"
            ))
        )

        # select first option
        search_box.send_keys(Keys.ARROW_DOWN)
        search_box.send_keys(Keys.ENTER)

        # CLOSE dropdown properly
        search_box.send_keys(Keys.TAB)

        # wait dropdown disappears
        wait.until(
            EC.invisibility_of_element_located((
                By.XPATH,
                "//div[@id='userTabPane']//div[contains(@class,'choices__list--dropdown')]"
            ))
        )

        # click date
        date_input = wait.until(
            EC.element_to_be_clickable(self.DATE_RANGE)
        )
        date_input.click()

        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(
            date.today() - timedelta(days=7),
            date.today()
        )

        # start time
        Select(
            wait.until(
                EC.element_to_be_clickable(self.START_TIME)
            )
        ).select_by_visible_text("01:00:00")

        # end time
        Select(
            wait.until(
                EC.element_to_be_clickable(self.END_TIME)
            )
        ).select_by_visible_text("02:00:00")

        self.click(self.EXPORT_SUBMIT)

        wait.until(
            EC.visibility_of_element_located(
                self.EXPORT_SUCCESS
            )
        )

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