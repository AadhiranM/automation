from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker


class SAVariantListPage(BasePage):

    # =============================
    # BUTTONS
    # =============================
    CREATE_VARIANT_BTN = (By.XPATH, "//a[normalize-space()='Create Variants']")


    # =============================
    # SEARCH
    # =============================
    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    # =============================
    # ENTRIES PER PAGE
    # =============================
    ENTRIES_DROPDOWN = (By.XPATH, "//select[@name='crudTable_length']")

    # =============================
    # PAGINATION
    # =============================
    NEXT_BTN = (By.XPATH, "//a[text()='Next']")
    PREV_BTN = (By.XPATH, "//a[text()='Previous']")

    # =============================
    # TABLE
    # =============================
    FIRST_ROW = (By.XPATH, "(//table//tbody/tr)[1]")
    NO_DATA_ROW = (By.XPATH, "//td[contains(@class,'dataTables_empty')]")
    CREATED_AT_COL = (By.XPATH, "//table//tbody/tr/td[4]")  # ⚠️ adjust if needed

    # =============================
    # DATE FILTER
    # =============================
    INLINE_CREATED_AT = (By.XPATH, "//input[contains(@placeholder,'Created At')]")

    PAGE_LOADED_MARKER = (By.XPATH, "//table")
    # =============================
    # CREATED BY COLUMN
    # =============================
    CREATED_BY_TEXT = (By.XPATH, "//table//tbody/tr//span[@class='ms-2']")
    CATEGORY_COLUMN = (By.XPATH, "//table//tbody/tr/td[2]")

    # =============================
    # NAVIGATION
    # =============================
    def goto_page(self):
        self.driver.get("https://beta.digitathya.com/admin/variant?reset_filters=1")
        self.wait_for_results()

    def wait_for_results(self):
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_elements(*self.FIRST_ROW)
            or d.find_elements(*self.NO_DATA_ROW)
        )

    # =============================
    # ACTIONS
    # =============================
    def search(self, text):
        self.wait_for_page_loaded()

        # get old first row text (if exists)
        old_text = ""
        rows = self.driver.find_elements(*self.FIRST_ROW)
        if rows:
            old_text = rows[0].text

        self.type(self.SEARCH_BOX, text)
        self.click(self.SEARCH_BTN)

        # wait until table data changes
        WebDriverWait(self.driver, 10).until(
            lambda d: (
                    d.find_elements(*self.NO_DATA_ROW) or
                    (
                            d.find_elements(*self.FIRST_ROW) and
                            d.find_elements(*self.FIRST_ROW)[0].text != old_text
                    )
            )
        )

    def set_entries_per_page(self, value):
        dropdown = self.wait(self.ENTRIES_DROPDOWN)
        Select(dropdown).select_by_value(str(value))
        time.sleep(0.3)
        self.wait_for_results()

    def click_next(self):
        self.click(self.NEXT_BTN)
        self.wait_for_results()

    def click_previous(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PREV_BTN)
        ).click()
        self.wait_for_results()


    # =============================
    # HELPERS
    # =============================
    def is_row_present(self):
        return bool(self.driver.find_elements(*self.FIRST_ROW))

    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.PAGE_LOADED_MARKER)
        )

    def has_no_data_message(self):
        return bool(self.driver.find_elements(*self.NO_DATA_ROW))

    def get_no_data_message(self):
        return self.driver.find_element(*self.NO_DATA_ROW).text.strip()

    # =============================
    # CREATE VALIDATION
    # =============================
    def click_create(self):
        self.wait_for_page_loaded()
        self.click(self.CREATE_VARIANT_BTN)

    def wait_for_table_refresh(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
        )

    def is_variant_present(self, value):
        return WebDriverWait(self.driver, 15).until(
            lambda d: len(d.find_elements(
                By.XPATH,
                f"//table//td[contains(normalize-space(),'{value}')]"
            )) > 0
        )

    def is_created_by_present(self, username):
        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.CREATED_BY_TEXT)
        )

        return any(username.lower() in e.text.lower() for e in elements)

    def is_category_present(self, category_name):
        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.CATEGORY_COLUMN)
        )

        for e in elements:
            try:
                if category_name.lower() in e.text.lower():
                    return True
            except:
                return False

        return False