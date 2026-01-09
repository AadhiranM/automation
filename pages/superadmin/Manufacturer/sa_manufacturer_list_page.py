from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker


class SAManufacturerListPage(BasePage):

    # =====================================================================
    # 1. PAGE ACTION BUTTONS
    # =====================================================================
    ADD_MANUFACTURER_BTN = (By.XPATH, "//button[contains(text(),'Add Manufacturer')]")
    CREATE_BTN = (By.XPATH, "//button[contains(normalize-space(),'Create')]")

    # =====================================================================
    # 2. SEARCH
    # =====================================================================
    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    # =====================================================================
    # 3. STATUS FILTER
    # =====================================================================
    STATUS_SELECT = (By.ID, "idStatus")

    # =====================================================================
    # 4. ENTRIES PER PAGE
    # =====================================================================
    ENTRIES_DROPDOWN = (By.XPATH, "//select[@name='crudTable_length']")

    # =====================================================================
    # 5. PAGINATION
    # =====================================================================
    NEXT_BTN = (By.XPATH, "//a[text()='Next']")
    PREV_BTN = (By.XPATH, "//a[text()='Previous']")
    PAGE_NUMBER = "//a[text()='{}']"

    # =====================================================================
    # 6. TABLE
    # =====================================================================
    FIRST_ROW = (By.XPATH, "(//table[contains(@class,'table')]//tbody/tr)[1]")
    NO_DATA_ROW = (By.XPATH, "//td[contains(@class,'dataTables_empty')]")
    CREATED_AT_COL = (By.XPATH, "//table//tbody/tr/td[5]")

    # =====================================================================
    # 7. ACTION MENU
    # =====================================================================
    ACTION_BTN = (By.CSS_SELECTOR, "div.dropdown > button.btn > i.ri-more-fill")
    ACTION_VIEW = (By.XPATH, "//a[normalize-space()='View']")
    ACTION_EDIT = (By.XPATH, "//a[normalize-space()='Edit']")
    ACTION_SEND_INVITE = (By.XPATH, "//a[contains(@class,'send-invite-btn')]")

    # =====================================================================
    # 8. SEND INVITE CONFIRMATION
    # =====================================================================
    SEND_INVITE_CONFIRM_BTN = (
        By.XPATH,
        "//button[contains(@class,'swal2-confirm') and normalize-space()='Send Invite!']"
    )
    INVITE_SUCCESS_OK_BTN = (
        By.XPATH,
        "//button[contains(@class,'swal2-confirm') and normalize-space()='OK']"
    )

    # =====================================================================
    # 9. DATE FILTER
    # =====================================================================
    INLINE_CREATED_AT = (By.XPATH, "//input[@placeholder='Filter by : Created At']")

    # =====================================================================
    # 10. PAGE LOAD MARKERS
    # =====================================================================
    PAGE_LOADED_MARKER = (By.XPATH, "//table[contains(@class,'dataTable')]")

    # =====================================================================
    # 11. NAVIGATION
    # =====================================================================
    def goto_page(self):
        """Navigate to Manufacturer List page"""
        self.driver.get(
            "https://beta.digitathya.com/admin/manufacturer?reset_filters=1"
        )
        self.wait_for_results()

    def wait_for_results(self):
        """Wait until table rows or no-data message appears"""
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_elements(*self.FIRST_ROW)
            or d.find_elements(*self.NO_DATA_ROW)
        )

    # =====================================================================
    # 🔹 11. USER ACTIONS (SEARCH / FILTER / PAGINATION)
    # =====================================================================
    def click_add_manufacturer(self):
        """Click 'Add Manufacturer' button"""
        self.click(self.ADD_MANUFACTURER_BTN)

    def click_create(self):
        """Click 'Create' button to open Create Manufacturer modal"""
        self.click(self.CREATE_BTN)

    def search(self, text):
        """
        Search manufacturer by keyword (company / email)
        """
        self.wait_for_page_loaded()
        self.type(self.SEARCH_BOX, text)
        self.click(self.SEARCH_BTN)
        self.wait_for_results()

    def filter_by_status(self, status):
        """
        Filter manufacturer list by status (Pending / Approved / Rejected)
        """
        dropdown = self.wait(self.STATUS_SELECT)
        Select(dropdown).select_by_visible_text(status)
        self.click(self.SEARCH_BTN)
        self.wait_for_results()

    def set_entries_per_page(self, value):
        """
        Set number of rows per page (10 / 25 / 50 / 100)
        """
        dropdown = self.wait(self.ENTRIES_DROPDOWN)
        Select(dropdown).select_by_value(str(value))
        time.sleep(0.4)
        self.wait_for_results()

    def click_next(self):
        """Go to next pagination page"""
        self.click(self.NEXT_BTN)
        self.wait_for_results()

    def click_previous(self):
        """Go to previous pagination page"""
        self.click(self.PREV_BTN)
        self.wait_for_results()

    def go_to_page(self, number):
        """Navigate to specific page number"""
        self.click((By.XPATH, self.PAGE_NUMBER.format(number)))
        self.wait_for_results()

    # =====================================================================
    # 12. ACTION MENU OPERATIONS
    # =====================================================================
    def open_action_menu(self):
        self.click(self.ACTION_BTN)

    def click_view(self):
        self.click(self.ACTION_VIEW)

    def click_edit(self):
        self.click(self.ACTION_EDIT)

    def click_send_invite(self):
        self.click(self.ACTION_SEND_INVITE)

    def confirm_send_invite(self):
        self.wait(self.SEND_INVITE_CONFIRM_BTN)
        self.click(self.SEND_INVITE_CONFIRM_BTN)

    def accept_invite_success(self):
        self.wait(self.INVITE_SUCCESS_OK_BTN)
        self.click(self.INVITE_SUCCESS_OK_BTN)

    # =====================================================================
    # 13. DATE FILTER LOGIC
    # =====================================================================
    def filter_inline_created_at(self, start, end):
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

    # =====================================================================
    # 14. HELPERS / VALIDATIONS
    # =====================================================================
    def is_row_present(self):
        return bool(self.driver.find_elements(*self.FIRST_ROW))

    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.PAGE_LOADED_MARKER)
        )

    def has_no_data_message(self):
        return bool(self.driver.find_elements(*self.NO_DATA_ROW))

    def get_no_data_message(self):
        el = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.NO_DATA_ROW)
        )
        return el.text.strip()

    def is_company_present(self, company_name):
        """
        Check whether a company name exists in the table
        """
        self.search(company_name)

        rows = self.driver.find_elements(
            By.XPATH,
            f"//table//tbody//td[normalize-space()='{company_name}']"
        )

        return len(rows) > 0
