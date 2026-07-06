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


class SANotScannableFeedbackPage(BasePage):

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


    EXPORT_CSV = (By.XPATH, "//a[contains(text(),'Export as Csv')]")
    DATE_INPUT = (By.XPATH, "//input[@placeholder='Select date']")
    DATE_SUBMIT = (By.XPATH, "//button[contains(text(),'Submit')]")

    # ======================================================
    # NAVIGATION
    # ======================================================
    def goto_page(self):
        self.driver.get(
            "https://beta.digitathya.com/admin/qr-notscannable-product-feedback?reset_filters=1"
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

        dropdown = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "idStatus"))
        )

        Select(dropdown).select_by_visible_text(status)

        self.click(self.SEARCH_BTN)  # or SEARCH_BTN, whichever your page uses
        self.wait_for_results()

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
    def view_feedback(self):
        wait = WebDriverWait(self.driver, 20)

        action_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "(//table/tbody/tr[1]//button[contains(@class,'dropdown')])[1]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            action_btn
        )

        print("Action dropdown clicked")

        view_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//ul[contains(@class,'dropdown-menu') and contains(@class,'show')]//a[contains(.,'View')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            view_btn
        )

        print("View clicked")

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
            (By.XPATH, "//table/tbody/tr[1]/td[5]")
        ).strip()

        print(f"PRODUCT FROM TABLE = {product_name}")
        # get product from list page

        # Product not available
        if product_name.upper() == "N/A" or product_name == "-":
            print("Manufacturer has no product. Skipping edit.")
            return None
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

        # Check manufacturer
        manufacturer = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//table/tbody/tr[1]/td[4]")
            )
        ).text.strip()

        print(f"MANUFACTURER = {manufacturer}")

        if manufacturer.upper() == "N/A" or manufacturer == "-":
            print("No manufacturer assigned for this record. Skipping assignment.")
            return None

        # First row scan id
        first_scan_id = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//table/tbody/tr[1]/td[2]")
            )
        ).text.strip()

        print(f"FIRST ROW SCAN ID = {first_scan_id}")

        # First row checkbox
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
            self.driver.execute_script(
                "arguments[0].click();",
                checkbox
            )

        print("Checkbox selected")
        time.sleep(1)

        # Assign Manufacturer button
        assign_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Assign Manufacturer')]")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            assign_btn
        )

        print("Assign Manufacturer clicked")

        time.sleep(5)

        rows = self.driver.find_elements(
            By.XPATH,
            f"//table/tbody/tr/td[contains(text(),'{first_scan_id}')]"
        )

        assert len(rows) == 0, (
            f"Scan ID still present after assignment: {first_scan_id}"
        )

        print("Manufacturer assigned successfully, row removed")

        return first_scan_id

    def export_csv_report(self):

        wait = WebDriverWait(self.driver, 30)
        downloads_path = os.path.join(os.getcwd(), "downloads")

        before_files = set(
            glob.glob(os.path.join(downloads_path, "*.csv"))
        )

        # -----------------------------
        # Export button
        # -----------------------------
        export_btn = wait.until(
            EC.element_to_be_clickable(self.EXPORT_BTN)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            export_btn
        )

        print("Export button clicked")

        # -----------------------------
        # Export CSV
        # -----------------------------
        export_csv = wait.until(
            EC.element_to_be_clickable(self.EXPORT_CSV)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            export_csv
        )

        print("Export CSV clicked")

        # -----------------------------
        # Wait for popup
        # -----------------------------

        time.sleep(2)

        print(self.driver.page_source.find("dateRangeModal"))
        print(self.driver.page_source.find("FakedateRangeModal"))

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "dateRangeModal")
            )
        )

        print("Date popup opened")

        # -----------------------------
        # Open Calendar
        # -----------------------------
        self.safe_click(self.DATE_INPUT)

        # -----------------------------
        # Select Last 7 Days
        # -----------------------------
        start = date.today() - timedelta(days=7)
        end = date.today()

        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(start, end)

        print(f"Selected Date Range : {start} -> {end}")

        # -----------------------------
        # Submit
        # -----------------------------
        submit_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[@id='dateRangeModal']//button[@type='submit']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            submit_btn
        )

        print("Export Submit clicked")

        # -----------------------------
        # Wait for Download
        # -----------------------------
        downloaded = False

        for _ in range(30):

            time.sleep(2)

            after_files = set(
                glob.glob(os.path.join(downloads_path, "*.csv"))
            )

            new_files = after_files - before_files

            if new_files:
                downloaded = True
                print("CSV Downloaded Successfully")
                break

        assert downloaded, f"CSV file not downloaded in {downloads_path}"