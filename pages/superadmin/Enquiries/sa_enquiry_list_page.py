from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker


class SAEnquiryListPage(BasePage):

    # ----------------- SEARCH -----------------
    SEARCH_BOX = (By.ID, "search-vale")

    # ----------------- STATUS FILTER -----------------
    STATUS_SELECT = (By.ID, "idStatus")   # Native <select>
    STATUS_OPTION = "//select[@id='idStatus']/option[text()='{}']"

    # ----------------- ENTRIES PER PAGE -----------------
    ENTRIES_DROPDOWN = (By.XPATH, "//select[@name='crudTable_length']")
    ENTRIES_OPTION = "//select[@name='crudTable_length']/option[@value='{}']"

    # ----------------- PAGINATION -----------------
    NEXT_BTN = (By.XPATH, "//a[text()='Next']")
    PREV_BTN = (By.XPATH, "//a[text()='Previous']")
    PAGE_NUMBER = "//a[text()='{}']"

    # ----------------- TABLE -----------------
    FIRST_ROW = (By.XPATH, "(//table[contains(@class,'table')]//tbody/tr)[1]")
    NO_DATA_ROW = (By.XPATH, "//td[contains(@class,'dataTables_empty')]")
    CREATED_AT_COL = (By.XPATH, "//table[contains(@class,'table')]//tbody/tr/td[8]")

    # ----------------- ACTIONS -----------------
    # IMPORTANT FIX: Correct 3-dots button locator
    ACTION_BTN = (By.CSS_SELECTOR, "div.dropdown > button.btn > i.ri-more-fill")

    ACTION_VIEW = (By.XPATH, "//a[normalize-space()='View']")
    ACTION_EDIT = (By.XPATH, "//a[normalize-space()='Edit']")

    # ----------------- DATE FILTERS -----------------
    INLINE_CREATED_AT = (By.XPATH, "//input[@placeholder='Filter by : Created At']")
    FILTER_PANEL_BTN = (By.ID, "filterToggleBtn")
    PANEL_DATE_RANGE = (By.ID, "date_range")
    APPLY_BTN = (By.XPATH, "//button[normalize-space()='Apply']")
    CLEAR_BTN = (By.XPATH, "//button[normalize-space()='Clear Filter']")
    FILTER_CLOSE_ICON = (By.CSS_SELECTOR, "div.offcanvas-header button.close")

    STATUS_BADGE = (By.XPATH, "//table//tbody/tr[1]//td[5]//span")

    PAGE_LOADED_MARKER = (
        By.XPATH, "//table[contains(@class,'dataTable')]"
    )

    # ----------------- NAVIGATION -----------------
    def goto_page(self):
        self.driver.get("https://beta.digitathya.com/admin/enquires?reset_filters=1")
        self.wait_for_results()

    def wait_for_results(self):
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_elements(*self.FIRST_ROW)
                      or d.find_elements(*self.NO_DATA_ROW)
        )

    def wait_first_row_loaded(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_elements(*self.FIRST_ROW)
                      or d.find_elements(*self.NO_DATA_ROW)
        )

    # ----------------- SEARCH -----------------
    def search(self, text):
        self.wait_for_page_loaded()  # 👈 critical
        self.wait(self.SEARCH_BOX)
        self.type(self.SEARCH_BOX, text)
        self.driver.find_element(*self.SEARCH_BOX).send_keys("\n")

    # ----------------- STATUS FILTER -----------------
    def filter_by_status(self, status_text):
        dropdown = self.wait(self.STATUS_SELECT)
        Select(dropdown).select_by_visible_text(status_text)
        time.sleep(0.4)
        self.wait_for_results()

    # ----------------- ENTRIES PER PAGE -----------------
    def set_entries_per_page(self, value):
        dropdown = self.wait(self.ENTRIES_DROPDOWN)
        Select(dropdown).select_by_value(str(value))
        time.sleep(0.4)
        self.wait_for_results()

    # ----------------- PAGINATION -----------------
    def click_next(self):
        self.click(self.NEXT_BTN)
        time.sleep(0.4)
        self.wait_for_results()

    def click_previous(self):
        self.click(self.PREV_BTN)
        time.sleep(0.4)
        self.wait_for_results()

    def go_to_page(self, number):
        locator = (By.XPATH, self.PAGE_NUMBER.format(number))
        self.click(locator)
        time.sleep(0.4)
        self.wait_for_results()

    # ----------------- ACTION MENU -----------------
    def open_action_menu(self):
        self.click(self.ACTION_BTN)

    def click_view(self):
        self.click(self.ACTION_VIEW)

    def click_edit(self):
        self.click(self.ACTION_EDIT)

    # ----------------- CREATED DATE HANDLER -----------------
    def get_all_created_dates(self):
        rows = self.driver.find_elements(*self.CREATED_AT_COL)
        result = []
        for r in rows:
            try:
                dt = datetime.strptime(r.text.strip(), "%d %b %Y %I:%M %p").date()
                result.append(dt)
            except:
                pass
        return result

    # ----------------- INLINE DATE FILTER -----------------
    def filter_inline_created_at(self, start, end):
        self.click(self.INLINE_CREATED_AT)
        picker = FlatpickrRangePicker(self.driver)
        ok = picker.select_range(start, end)
        time.sleep(0.4)
        self.wait_for_results()
        return ok

    # ----------------- PANEL DATE FILTER -----------------
    def filter_panel_created_at(self, start, end):
        self.click(self.FILTER_PANEL_BTN)
        time.sleep(0.3)

        self.click(self.PANEL_DATE_RANGE)
        picker = FlatpickrRangePicker(self.driver)
        ok = picker.select_range(start, end)

        self.click(self.APPLY_BTN)
        self.close_filter_panel()
        self.wait_for_results()
        return ok

    # ----------------- HELPERS -----------------
    def is_row_present(self):
        return bool(self.driver.find_elements(*self.FIRST_ROW))

    def has_no_results(self):
        return bool(self.driver.find_elements(*self.NO_DATA_ROW))

    def close_filter_panel(self):
        try:
            if self.driver.find_elements(*self.FILTER_CLOSE_ICON):
                self.click(self.FILTER_CLOSE_ICON)
        except:
            pass

    def get_first_row_status(self):
        el = self.wait(self.STATUS_BADGE)
        return el.text.strip()


    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.PAGE_LOADED_MARKER)
        )
