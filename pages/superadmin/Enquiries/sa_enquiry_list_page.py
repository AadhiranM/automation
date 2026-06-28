import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class SAEnquiryListPage(BasePage):

    # =====================================================
    # SEARCH
    # =====================================================

    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    # =====================================================
    # FILTERS
    # =====================================================

    INLINE_DATE_FILTER = (
        By.XPATH,
        "//input[@placeholder='Filter by : Created At']"
    )

    FILTER_PANEL_BTN = (
        By.ID,
        "filterToggleBtn"
    )

    PANEL_DATE_FILTER = (
        By.ID,
        "date_range"
    )

    APPLY_BTN = (
        By.XPATH,
        "//button[normalize-space()='Apply']"
    )

    CLEAR_FILTER_BTN = (
        By.XPATH,
        "//button[contains(text(),'Clear Filter')]"
    )

    STATUS_DROPDOWN = (
        By.ID,
        "idStatus"
    )

    FILTER_CLOSE_ICON = (
        By.CSS_SELECTOR,
        ".offcanvas-header button"
    )

    # =====================================================
    # TABLE
    # =====================================================

    FIRST_ROW = (
        By.XPATH,
        "//table/tbody/tr[1]"
    )

    NO_DATA = (
        By.XPATH,
        "//td[contains(@class,'dataTables_empty')]"
    )

    FIRST_ROW_ID = (
        By.XPATH,
        "//table/tbody/tr[1]/td[1]"
    )

    FIRST_ROW_NAME = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    FIRST_ROW_EMAIL = (
        By.XPATH,
        "//table/tbody/tr[1]/td[3]"
    )

    FIRST_ROW_COMPANY = (
        By.XPATH,
        "//table/tbody/tr[1]/td[4]"
    )

    FIRST_ROW_STATUS = (
        By.XPATH,
        "//table/tbody/tr[1]/td[5]//span"
    )

    CREATED_AT_COLUMN = (
        By.XPATH,
        "//table/tbody/tr/td[8]"
    )

    # =====================================================
    # ACTIONS
    # =====================================================

    FIRST_ROW_THREE_DOTS = (
        By.XPATH,
        "//table/tbody/tr[1]/td[last()]//button"
    )

    VIEW_OPTION = (
        By.XPATH,
        "//a[contains(.,'View')]"
    )

    EDIT_OPTION = (
        By.XPATH,
        "//table/tbody/tr[1]//a[contains(normalize-space(),'Edit')]"
    )

    SEND_EMAIL_OPTION = (
        By.XPATH,
        "//a[@class='dropdown-item' and normalize-space()='Send Email']"
    )

    FOLLOW_UP_OPTION = (
        By.XPATH,
        "//a[@class='dropdown-item' and normalize-space()='Follow Up']"
    )

    # =====================================================
    # ENTRIES
    # =====================================================

    ENTRIES_DROPDOWN = (
        By.NAME,
        "crudTable_length"
    )

    # =====================================================
    # PAGINATION
    # =====================================================

    NEXT_BTN = (
        By.XPATH,
        "//a[normalize-space()='Next']"
    )

    PREVIOUS_BTN = (
        By.XPATH,
        "//a[normalize-space()='Previous']"
    )

    PAGE_NUMBER = (
        "//a[normalize-space()='{}']"
    )

    # =====================================================
    # PAGE LOAD
    # =====================================================

    PAGE_LOADED_MARKER = (
        By.ID,
        "crudTable"
    )

    # ==========================
    # PANEL FILTER
    # ==========================

    PANEL_NAME = (
        By.NAME,
        "name"
    )

    PANEL_EMAIL = (
        By.NAME,
        "business_email"
    )

    PANEL_COMPANY = (
        By.NAME,
        "company"
    )

    # PANEL_STATUS = (
    #     By.XPATH,
    #     "//label[contains(text(),'Status')]/following::div[contains(@class,'choices')][1]"
    # )

    PANEL_STATUS = (
        By.XPATH,
        "//label[normalize-space()='Status']/following::div[contains(@class,'choices')][1]"
    )

    PANEL_STATUS_OPTION = (
        "//li[contains(text(),'{}')]"
    )


    def get_first_row_id(self):
        return self.get_text(self.FIRST_ROW_ID).strip()

    def get_first_row_name(self):
        return self.get_text(self.FIRST_ROW_NAME).strip()

    def get_first_row_email(self):
        return self.get_text(self.FIRST_ROW_EMAIL).strip()

    def get_first_row_company(self):
        return self.get_text(self.FIRST_ROW_COMPANY).strip()

    def get_first_row_status(self):
        return self.get_text(self.FIRST_ROW_STATUS).strip()

    # =====================================================
    # NAVIGATION
    # =====================================================

    def open_filter_panel(self):

        self.click(
            self.FILTER_PANEL_BTN
        )

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                self.PANEL_NAME
            )
        )

    def panel_filter_by_name(
            self,
            name
    ):

        self.open_filter_panel()

        self.type(
            self.PANEL_NAME,
            name
        )

        self.click(
            self.APPLY_BTN
        )

        self.wait_for_results()

    def panel_filter_by_email(
            self,
            email
    ):

        self.open_filter_panel()

        self.type(
            self.PANEL_EMAIL,
            email
        )

        self.click(
            self.APPLY_BTN
        )

        self.wait_for_results()

    def panel_filter_by_company(
            self,
            company
    ):

        self.open_filter_panel()

        self.type(
            self.PANEL_COMPANY,
            company
        )

        self.click(
            self.APPLY_BTN
        )

        self.wait_for_results()

    def goto_page(self):

        self.driver.get(
            "https://beta.digitathya.com/admin/enquires?reset_filters=1"
        )

        self.wait_for_results()

    # =====================================================
    # WAITS
    # =====================================================



    def panel_filter_select_first_status(self):

        self.open_filter_panel()

        wait = WebDriverWait(
            self.driver,
            20
        )

        dropdown = wait.until(
            EC.element_to_be_clickable(
                self.PANEL_STATUS
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            dropdown
        )

        time.sleep(1)

        active = self.driver.switch_to.active_element

        active.send_keys(Keys.ENTER)
        selected_status = self.get_text(
            self.PANEL_STATUS
        ).strip()
        time.sleep(1)

        self.click(self.APPLY_BTN)

        self.wait_for_results()
        return selected_status


    def wait_for_results(self):

        WebDriverWait(self.driver, 15).until(
            lambda d:
            d.find_elements(*self.FIRST_ROW)
            or
            d.find_elements(*self.NO_DATA)
        )

    def wait_for_page_loaded(self):

        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                self.PAGE_LOADED_MARKER
            )
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search(self, text):

        self.type(self.SEARCH_BOX, text)

        self.click(self.SEARCH_BTN)

        self.wait_for_results()

    def search_first_enquiry_name(self):

        name = self.get_first_row_name()

        self.search(name)

        return name

    def search_first_enquiry_email(self):

        email = self.get_first_row_email()

        self.search(email)

        return email

    # =====================================================
    # GETTERS
    # =====================================================


    # STATUS FILTER
    # =====================================================

    def filter_by_status(self, status):

        dropdown = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                self.STATUS_DROPDOWN
            )
        )

        Select(dropdown).select_by_visible_text(status)

        self.wait_for_results()

    # =====================================================
    # DATE FILTER
    # =====================================================

    def filter_inline_created_at(self, start, end):


        self.safe_click(self.INLINE_DATE_FILTER)

        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(start, end)

        self.click(self.SEARCH_BTN)

        self.wait_for_results()

    def filter_panel_select_range(self, start, end):

        self.open_filter_panel()

        self.safe_click(self.PANEL_DATE_FILTER)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                FlatpickrRangePicker.CALENDAR
            )
        )

        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(start, end)

        self.click(self.APPLY_BTN)

        self.wait_for_results()

    def close_filter_panel(self):

        try:

            if self.driver.find_elements(
                    *self.FILTER_CLOSE_ICON
            ):
                self.click(
                    self.FILTER_CLOSE_ICON
                )

        except:
            pass

    # =====================================================
    # ENTRIES
    # =====================================================

    def set_entries_per_page(self, value):

        dropdown = Select(
            self.driver.find_element(
                *self.ENTRIES_DROPDOWN
            )
        )

        dropdown.select_by_value(
            str(value)
        )

        self.wait_for_results()

    # =====================================================
    # PAGINATION
    # =====================================================

    def click_next(self):

        self.click(
            self.NEXT_BTN
        )

        self.wait_for_results()

    def click_previous(self):

        self.click(
            self.PREVIOUS_BTN
        )

        self.wait_for_results()

    def go_to_page(self, number):

        self.click((
            By.XPATH,
            self.PAGE_NUMBER.format(number)
        ))

        self.wait_for_results()

    # =====================================================
    # ACTIONS
    # =====================================================

    def open_first_row_actions(self):

        self.click(self.FIRST_ROW_THREE_DOTS)

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                self.EDIT_OPTION
            )
        )
    def click_edit(self):

        print("Inside click_edit")

        self.open_first_row_actions()

        print("Menu opened")

        self.click(self.EDIT_OPTION)

        print("Edit clicked")

    def click_view(self):

        self.open_first_row_actions()

        self.click(
            self.VIEW_OPTION
        )


    def click_send_email(self):

        self.open_first_row_actions()

        self.click(
            self.SEND_EMAIL_OPTION
        )


    def click_follow_up(self):

        self.open_first_row_actions()

        followup = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.FOLLOW_UP_OPTION)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            followup
        )

        self.driver.execute_script(
            "arguments[0].click();",
            followup
        )

    # =====================================================
    # VALIDATIONS
    # =====================================================

    def is_row_present(self):

        return len(
            self.driver.find_elements(
                *self.FIRST_ROW
            )
        ) > 0

    def has_no_data(self):

        return len(
            self.driver.find_elements(
                *self.NO_DATA
            )
        ) > 0

    def get_all_created_dates(self):

        rows = self.driver.find_elements(
            *self.CREATED_AT_COLUMN
        )

        dates = []

        for row in rows:

            try:

                dt = datetime.strptime(
                    row.text.strip(),
                    "%d %b %Y %I:%M %p"
                ).date()

                dates.append(dt)

            except Exception:
                pass

        return dates

    def verify_search_result(self, expected_text):

        row_text = self.get_text(
            self.FIRST_ROW
        )

        return expected_text.lower() in row_text.lower()

