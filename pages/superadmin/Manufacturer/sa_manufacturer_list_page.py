from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker


class SAManufacturerListPage(BasePage):

    # ----------------- SEARCH -----------------
    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    NO_DATA_ROW = (By.CSS_SELECTOR, "td.dataTables_empty")

    # ----------------- STATUS FILTER -----------------
    STATUS_SELECT = (By.ID, "idStatus")
    STATUS_OPTION = "//select[@id='idStatus']/option[normalize-space()='{}']"

    # ----------------- ENTRIES PER PAGE -----------------
    ENTRIES_DROPDOWN = (By.XPATH, "//select[@name='crudTable_length']")

    # ----------------- PAGINATION -----------------
    NEXT_BTN = (By.XPATH, "//a[text()='Next']")
    PREV_BTN = (By.XPATH, "//a[text()='Previous']")
    PAGE_NUMBER = "//a[text()='{}']"

    # ----------------- TABLE -----------------
    FIRST_ROW = (By.XPATH, "(//table[contains(@class,'table')]//tbody/tr[1])")
    NO_DATA_ROW = (By.XPATH, "//td[contains(@class,'dataTables_empty')]")
    CREATED_AT_COL = (By.XPATH, "//table//tbody/tr/td[5]")

    # ----------------- ACTIONS -----------------
    ACTION_BTN = (By.CSS_SELECTOR, "div.dropdown > button.btn > i.ri-more-fill")

    ACTION_VIEW = (By.XPATH, "//a[normalize-space()='View']")
    ACTION_EDIT = (By.XPATH, "//a[normalize-space()='Edit']")
    ACTION_SEND_INVITE = (
        By.XPATH,
        "//a[contains(@class,'send-invite-btn')]"
    )

    # ----------------- DATE FILTER -----------------
    INLINE_CREATED_AT = (By.XPATH, "//input[@placeholder='Filter by : Created At']")

    PAGE_LOADED_MARKER = (
        By.XPATH, "//table[contains(@class,'dataTable')]"
    )

    # ----------------- NAVIGATION -----------------
    def goto_page(self):
        self.driver.get(
            "https://beta.digitathya.com/admin/manufacturer?reset_filters=1"
        )
        self.wait_for_results()

    def wait_for_results(self):
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_elements(*self.FIRST_ROW)
            or d.find_elements(*self.NO_DATA_ROW)
        )

    # ----------------- SEARCH -----------------
    def search(self, text):
        self.wait_for_page_loaded()
        self.type(self.SEARCH_BOX, text)
        self.click(self.SEARCH_BTN)  # 🔑 important
        self.wait_for_results()

    # ----------------- STATUS FILTER -----------------
    def filter_by_status(self, status):
        dropdown = self.wait(self.STATUS_SELECT)
        Select(dropdown).select_by_visible_text(status)
        self.click(self.SEARCH_BTN)  # 🔑 required
        self.wait_for_results()

    # ----------------- ENTRIES -----------------
    def set_entries_per_page(self, value):
        dropdown = self.wait(self.ENTRIES_DROPDOWN)
        Select(dropdown).select_by_value(str(value))
        time.sleep(0.4)
        self.wait_for_results()

    # ----------------- PAGINATION -----------------
    def click_next(self):
        self.click(self.NEXT_BTN)
        self.wait_for_results()

    def click_previous(self):
        self.click(self.PREV_BTN)
        self.wait_for_results()

    def go_to_page(self, number):
        self.click((By.XPATH, self.PAGE_NUMBER.format(number)))
        self.wait_for_results()

    # ----------------- ACTION MENU -----------------
    def open_action_menu(self):
        self.click(self.ACTION_BTN)

    def click_view(self):
        self.click(self.ACTION_VIEW)

    def click_edit(self):
        self.click(self.ACTION_EDIT)

    def click_send_invite(self):
        self.click(self.ACTION_SEND_INVITE)

    # ----------------- DATE FILTER -----------------
    def filter_inline_created_at(self, start, end):
        # 1. Find the date input
        date_input = self.driver.find_element(*self.INLINE_CREATED_AT)

        # 2. Click the input to open calendar
        date_input.click()

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flatpickr-calendar"))
        )

        # 3. (Optional) visually select range
        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(start, end)

        # 4. 🔑 FORCE SET VALUE EXACTLY AS BACKEND EXPECTS
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

        # 🔍 DEBUG (KEEP FOR NOW)
        print("Date input value:", date_input.get_attribute("value"))

        # 5. Click Search button
        self.click(self.SEARCH_BTN)

        # 🔍 DEBUG (KEEP FOR NOW)
        print("URL after search:", self.driver.current_url)

        # 6. Wait for table reload
        self.wait_for_results()

    def get_all_created_dates(self):
        rows = self.driver.find_elements(*self.CREATED_AT_COL)
        result = []
        for r in rows:
            try:
                result.append(
                    datetime.strptime(
                        r.text.strip(), "%d %b %Y %I:%M %p"
                    ).date()
                )
            except:
                pass
        return result

    # ----------------- HELPERS -----------------
    def is_row_present(self):
        return bool(self.driver.find_elements(*self.FIRST_ROW))

    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.PAGE_LOADED_MARKER)
        )

    def has_no_data_message(self):
        elements = self.driver.find_elements(*self.NO_DATA_ROW)
        return bool(elements)

    def get_no_data_message(self):
        el = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.NO_DATA_ROW)
        )
        return el.text.strip()
