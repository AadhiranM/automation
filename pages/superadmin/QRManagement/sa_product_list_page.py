import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker


class SAProductListPage(BasePage):

    # =============================
    # SEARCH
    # =============================
    SEARCH_BOX = (By.XPATH, "//input[contains(@placeholder,'Search')]")
    SEARCH_BTN = (By.XPATH, "//button[contains(@class,'search')]")

    # =============================
    # FILTERS
    # =============================
    STATUS_DROPDOWN = (By.ID, "select2-idStatus-container")
    STATUS_OPTIONS = (By.XPATH, "//ul[contains(@class,'select2-results__options')]")
    STATUS_OPTION = "//li[contains(@class,'select2-results__option') and normalize-space()='{}']"

    INLINE_CREATED_AT = (By.XPATH, "//input[@placeholder='Created At']")

    # =============================
    # ENTRIES
    # =============================
    ENTRIES_DROPDOWN = (By.NAME, "crudTable_length")

    # =============================
    # PAGINATION
    # =============================
    NEXT_BTN = (By.XPATH, "//a[normalize-space()='Next']")
    PREV_BTN = (By.XPATH, "//a[normalize-space()='Previous']")
    PAGE_NUMBER = "//a[normalize-space()='{}']"

    # =============================
    # TABLE
    # =============================
    FIRST_ROW = (By.XPATH, "//table/tbody/tr[1]")
    NO_DATA = (By.XPATH, "//td[contains(@class,'dataTables_empty')]")
    CREATED_AT_COL = (By.XPATH, "//table//tbody/tr/td[last()-1]")
    CREATE_BTN = (By.XPATH, "//a[normalize-space()='Create']")

    FIRST_PRODUCT_NAME = (
        By.XPATH,
        "//tbody/tr[1]/td[2]"
    )


    # =============================
    # NAVIGATION
    # =============================
    def goto_page(self):
        self.driver.get("https://beta.digitathya.com/admin/product?reset_filters=1")
        self.wait_for_results()

    def wait_for_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h5[contains(text(),'List')]")
            )
        )

    def get_first_product_name(self):
        return self.get_text(self.FIRST_PRODUCT_NAME).strip()

    def wait_for_results(self):
        WebDriverWait(self.driver, 15).until(
            lambda d: d.find_elements(*self.FIRST_ROW) or d.find_elements(*self.NO_DATA)
        )

    # =============================
    # ACTIONS
    # =============================
    def search(self, text):
        self.type(self.SEARCH_BOX, text)
        self.click(self.SEARCH_BTN)
        self.wait_for_results()

    # 🔥 SELECT2 FIX
    def filter_by_status(self, status):
        self.click(self.STATUS_DROPDOWN)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.STATUS_OPTIONS)
        )

        option = (By.XPATH, self.STATUS_OPTION.format(status))
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(option)
        ).click()

        self.wait_for_results()

    def set_entries_per_page(self, value):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.ENTRIES_DROPDOWN)
        )
        Select(dropdown).select_by_value(str(value))
        self.wait_for_results()

    # PAGINATION FIX
    def click_next(self):
        self.close_calendar()  # ✅ FIX

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]")
            )
        )

        next_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.NEXT_BTN)
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_btn)
        self.driver.execute_script("arguments[0].click();", next_btn)

        self.wait_for_results()

    def click_previous(self):
        self.close_calendar()

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]")
            )
        )

        # RE-FIND element (avoid stale)
        prev_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PREV_BTN)
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", prev_btn)
        self.driver.execute_script("arguments[0].click();", prev_btn)

        self.wait_for_results()

    def go_to_page(self, number):
        self.close_calendar()

        page_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.PAGE_NUMBER.format(number))
            )
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", page_btn)
        self.driver.execute_script("arguments[0].click();", page_btn)

        self.wait_for_results()

    # =============================
    # DATE FILTER (FLATPICKR FIX)
    # =============================
    def filter_created_date(self, start, end):
        date_input = self.driver.find_element(*self.INLINE_CREATED_AT)
        date_input.click()

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flatpickr-calendar"))
        )

        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(start, end)

        date_value = f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}"
        self.driver.execute_script(
            """
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
            arguments[0].dispatchEvent(new Event('blur'));
            """,
            date_input,
            date_value
        )

        self.click(self.SEARCH_BTN)
        self.wait_for_results()

    def get_created_dates(self):
        rows = self.driver.find_elements(*self.CREATED_AT_COL)
        dates = []

        for r in rows:
            text = r.text.strip()
            try:
                parsed = datetime.strptime(text, "%d %b %Y %I:%M %p").date()
                dates.append(parsed)
            except:
                print(f"Skipping invalid date: {text}")

        return dates

    # =============================
    # VALIDATIONS
    # =============================
    def is_row_present(self):
        return len(self.driver.find_elements(*self.FIRST_ROW)) > 0

    def has_no_data(self):
        return len(self.driver.find_elements(*self.NO_DATA)) > 0

    def close_calendar(self):
        self.driver.execute_script("document.body.click();")


    def click_create(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CREATE_BTN)
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        self.driver.execute_script("arguments[0].click();", btn)

    def is_product_present(self, product_name):

        rows = self.driver.find_elements(
            By.XPATH,
            "//table//tbody//tr"
        )

        for row in rows:

            if product_name.lower() in row.text.lower():
                return True

        return False

    def is_sku_present(self, sku_id):

        rows = self.driver.find_elements(
            By.XPATH,
            "//table//tbody//tr"
        )

        for row in rows:

            if sku_id.lower() in row.text.lower():
                return True

        return False

    def get_first_product_data(self):

        manufacturer = self.get_text(
            (
                By.XPATH,
                "//table//tbody//tr[1]/td[3]"
            )
        )

        product_name = self.get_text(
            (
                By.XPATH,
                "//table//tbody//tr[1]/td[4]"
            )
        )

        sku_id = self.get_text(
            (
                By.XPATH,
                "//table//tbody//tr[1]/td[5]"
            )
        )

        return manufacturer, product_name, sku_id