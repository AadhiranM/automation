from datetime import date, timedelta
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker
from selenium.webdriver.common.action_chains import ActionChains
import os
import glob
from datetime import datetime, timedelta


class SAFakeProductFeedbackPage(BasePage):

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
    # THREE DOTS
    # ======================================================
    ACTIONS_BTN = (
        By.XPATH,
        "(//table/tbody/tr[1]//button[contains(@class,'btn')])[last()]"
    )

    EDIT_BTN = (
        By.XPATH,
        "//a[contains(.,'Edit')]"
    )

    VIEW_BTN = (
        By.XPATH,
        "//div[contains(@class,'dropdown-menu') and contains(@class,'show')]//a[normalize-space()='View']"
    )



    # ======================================================
    # EDIT PAGE
    # ======================================================
    PRODUCT_DROPDOWN = (
        By.XPATH,
        "//label[contains(text(),'Product')]/following::div[contains(@class,'choices__inner')][1]"
    )

    PRODUCT_SEARCH = (
        By.XPATH,
        "//input[contains(@class,'select2-search__field')]"
    )

    COMMENTS_BOX = (
        By.NAME,
        "comments"
    )

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
    EXPORT_BTN = (
        By.XPATH,
        "//button[contains(.,'Export')]"
    )


    EXPORT_CSV = (By.XPATH, "//a[contains(text(),'Export as CSV')]")
    DATE_INPUT = (By.XPATH, "//input[@placeholder='Select date']")
    DATE_SUBMIT = (By.XPATH, "//button[contains(text(),'Submit')]")

    # ======================================================
    # NAVIGATION
    # ======================================================
    def goto_page(self):
        self.driver.get(
            "https://beta.digitathya.com/admin/qr-fake-product-feedback?reset_filters=1"
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
    def open_view(self):

        self.click(self.ACTIONS_BTN)
        self.click(self.VIEW_BTN)

    # ======================================================
    # EDIT
    # ======================================================
    # ======================================================
    # EDIT
    # ==================

    def select_product_for_feedback(self, product_name):
        wait = WebDriverWait(self.driver, 30)

        print(f"PRODUCT TO SELECT = {product_name}")

        # click product dropdown
        dropdown = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[contains(text(),'Product')]/following::div[contains(@class,'choices')][1]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )
        time.sleep(2)

        ActionChains(self.driver).move_to_element(dropdown).click().perform()
        print("Product dropdown clicked")
        time.sleep(2)

        # TYPE DIRECTLY TO ACTIVE ELEMENT
        active = self.driver.switch_to.active_element

        partial = product_name[:20]

        for ch in partial:
            active.send_keys(ch)
            time.sleep(0.2)

        print(f"Typed product: {partial}")
        time.sleep(3)

        # exact option click
        option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//div[@role='option'][contains(., '{partial}')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'nearest'});",
            option
        )
        time.sleep(1)

        ActionChains(self.driver).move_to_element(option).click().perform()

        print("Product selected successfully")

        # verify hidden value got selected
        hidden = self.driver.find_element(
            By.NAME,
            "product_ref_id"
        ).get_attribute("value")

        print("Selected hidden value =", hidden)

        assert hidden.strip() != "", "Product was not selected"

        time.sleep(2)

    def edit_feedback(self):
        wait = WebDriverWait(self.driver, 30)

        # get product from list page
        product_name = self.get_text(
            (By.XPATH, "//table/tbody/tr[1]/td[6]")
        ).strip()

        print(f"PRODUCT FROM TABLE = {product_name}")

        # click actions
        actions = wait.until(
            EC.element_to_be_clickable(self.ACTIONS_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            actions
        )
        time.sleep(2)

        self.driver.execute_script("arguments[0].click();", actions)
        print("Actions clicked")
        time.sleep(2)

        # click edit
        edit_btn = wait.until(
            EC.element_to_be_clickable(self.EDIT_BTN)
        )

        self.driver.execute_script("arguments[0].click();", edit_btn)
        print("Edit clicked")

        # wait edit page
        wait.until(EC.url_contains("/edit"))
        time.sleep(5)

        print("Edit page fully loaded")

        # NOW select product
        self.select_product_for_feedback(product_name)

        comment = "Updated automation feedback"

        comment_box = wait.until(
            EC.element_to_be_clickable(self.COMMENTS_BOX)
        )

        comment_box.clear()
        comment_box.send_keys(comment)

        self.click(self.SUBMIT_BTN)

        wait.until(
            EC.visibility_of_element_located(self.SUCCESS_MSG)
        )

        return comment
    def export_records(self):

        self.click(self.EXPORT_BTN)

    # ======================================================
    # VALIDATIONS
    # ======================================================
    def is_row_present(self):

        return len(
            self.driver.find_elements(*self.FIRST_ROW)
        ) > 0

    def has_no_data(self):

        return len(
            self.driver.find_elements(*self.NO_DATA)
        ) > 0

    # ======================================================

    # HELPER METHODS

    def assign_manufacturer_and_verify_row_removed(self):
        wait = WebDriverWait(self.driver, 30)

        # first row scan id
        first_scan_id = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//table/tbody/tr[1]/td[2]")
            )
        ).text.strip()

        print(f"FIRST ROW SCAN ID = {first_scan_id}")

        # first row checkbox
        checkbox = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//table/tbody/tr[1]//input[@type='checkbox']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            checkbox
        )
        time.sleep(1)

        if not checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", checkbox)

        print("Checkbox selected")
        time.sleep(1)

        # assign manufacturer button
        assign_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Assign Manufacturer')]")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            assign_btn
        )
        time.sleep(1)

        self.driver.execute_script("arguments[0].click();", assign_btn)

        print("Assign Manufacturer clicked")

        # wait refresh
        time.sleep(5)

        # verify old scan id removed
        rows = self.driver.find_elements(
            By.XPATH,
            f"//table/tbody/tr/td[contains(text(),'{first_scan_id}')]"
        )

        assert len(rows) == 0, f"Scan ID still present after assignment: {first_scan_id}"

        print("Manufacturer assigned successfully, row removed")

        return first_scan_id

    def export_csv_report(self):
        wait = WebDriverWait(self.driver, 30)

        downloads_path = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        before_files = set(
            glob.glob(os.path.join(downloads_path, "*.csv"))
        )

        # export button
        export_btn = wait.until(
            EC.element_to_be_clickable(self.EXPORT_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            export_btn
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            export_btn
        )

        print("Export button clicked")

        # export csv option
        export_csv = wait.until(
            EC.element_to_be_clickable(self.EXPORT_CSV)
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            export_csv
        )

        print("Export CSV clicked")

        # wait for modal
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h5[contains(text(),'Select Date Range')]")
            )
        )

        print("Date popup opened")

        # yesterday to today
        today = datetime.today()
        yesterday = today - timedelta(days=1)

        from_date = yesterday.strftime("%d-%m-%Y")
        to_date = today.strftime("%d-%m-%Y")

        date_range = f"{from_date} to {to_date}"

        print("Date range selected:", date_range)

        # date input
        date_input = wait.until(
            EC.presence_of_element_located(self.DATE_INPUT)
        )

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
        """, date_input, date_range)

        print("Date entered:", date_range)

        time.sleep(2)

        # submit
        submit_btn = wait.until(
            EC.element_to_be_clickable(self.SUBMIT_BTN)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            submit_btn
        )

        print("Export submit clicked")

        # wait for download
        downloaded = False

        for i in range(30):
            files = glob.glob(
                os.path.join(downloads_path, "*.csv")
            )

            if len(files) > len(before_files):
                downloaded = True
                print("CSV downloaded successfully")
                break

            time.sleep(1)

        assert downloaded, f"CSV file not downloaded in {downloads_path}"