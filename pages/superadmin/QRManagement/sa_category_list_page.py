from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker


class SACategoryListPage(BasePage):

    # =====================================================================
    # 1. PAGE ACTION BUTTONS
    # =====================================================================
    CREATE_CATEGORY_BTN = (By.XPATH, "//button[normalize-space()='Create Category']")

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
    FIRST_ROW = (By.XPATH, "(//table//tbody/tr)[1]")
    NO_DATA_ROW = (By.XPATH, "//td[contains(@class,'dataTables_empty')]")
    CREATED_AT_COL = (By.XPATH, "//table//tbody/tr/td[6]")

    # =====================================================================
    # 7. ACTION MENU
    # =====================================================================
    ACTION_BTN = (By.CSS_SELECTOR, "div.dropdown > button.btn > i.ri-more-fill")
    ACTION_VIEW = (By.XPATH, "//a[normalize-space()='View']")
    ACTION_EDIT = (By.XPATH, "//a[normalize-space()='Edit']")

    # =====================================================================
    # 8. DATE FILTER
    # =====================================================================
    INLINE_CREATED_AT = (By.XPATH, "//input[@placeholder='Created At']")

    # =====================================================================
    # 9. PAGE LOAD MARKER
    # =====================================================================
    PAGE_LOADED_MARKER = (By.XPATH, "//table[contains(@class,'dataTable')]")

    # =====================================================================
    # 10. NAVIGATION
    # =====================================================================

    FIRST_ROW_CATEGORY = (
        By.XPATH,
        "//tbody/tr[1]/td[2]"
    )

    FIRST_ROW_STATUS = (
        By.XPATH,
        "//tbody/tr[1]/td[4]"
    )
    FIRST_MANUFACTURER_NAME = (
        By.XPATH,
        "//tbody/tr[1]/td[3]"
    )

    def get_first_manufacturer_name(self):
        return self.get_text(self.FIRST_MANUFACTURER_NAME).strip()

    def goto_page(self):
        self.driver.get(
            "https://beta.digitathya.com/admin/category?reset_filters=1"
        )
        self.wait_for_results()

    def wait_for_results(self):
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_elements(*self.FIRST_ROW)
            or d.find_elements(*self.NO_DATA_ROW)
        )

    # =====================================================================
    # 11. USER ACTIONS
    # =====================================================================
    def search(self, text):
        self.wait_for_page_loaded()
        self.type(self.SEARCH_BOX, text)
        self.click(self.SEARCH_BTN)
        self.wait_for_results()

    def filter_by_status(self, status):
        dropdown = self.wait(self.STATUS_SELECT)
        Select(dropdown).select_by_visible_text(status)
        self.click(self.SEARCH_BTN)
        self.wait_for_results()

    def set_entries_per_page(self, value):
        dropdown = self.wait(self.ENTRIES_DROPDOWN)
        Select(dropdown).select_by_value(str(value))
        time.sleep(0.3)
        self.wait_for_results()

    def click_next(self):
        self.click(self.NEXT_BTN)
        self.wait_for_results()

    def click_previous(self):
        self.click(self.PREV_BTN)
        self.wait_for_results()

    def go_to_page(self, number):
        self.click((By.XPATH, self.PAGE_NUMBER.format(number)))
        self.wait_for_results()

    # =====================================================================
    # 12. ACTION MENU
    # =====================================================================
    def open_action_menu(self):
        self.click(self.ACTION_BTN)


    def click_view(self):
        self.click(self.ACTION_VIEW)

    def click_edit(self):
        self.click(self.ACTION_EDIT)

    # =====================================================================
    # 13. DATE FILTER
    # =====================================================================
    def filter_inline_created_at(self, start, end):

        self.safe_click(self.INLINE_CREATED_AT)

        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(start, end)

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
    # 14. HELPERS
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
        return self.driver.find_element(*self.NO_DATA_ROW).text.strip()

    # =====================================================================
    # 15. CREATE + VALIDATION HELPERS
    # =====================================================================

    def click_create(self):
        self.click(self.CREATE_CATEGORY_BTN)

    def wait_for_table_refresh(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
        )

    def is_category_present(self, name):
        return WebDriverWait(self.driver, 15).until(
            lambda d: len(d.find_elements(
                By.XPATH,
                f"//table//td[contains(normalize-space(),'{name}')]"
            )) > 0
        )

    def get_category_status(self, name):
        rows = self.driver.find_elements(By.XPATH, "//table//tbody/tr")

        for row in rows:
            if name.lower() in row.text.lower():
                return row.find_element(By.XPATH, "./td[4]").text.strip()
                # Adjust column index if needed

        return None

    def get_first_active_category_name(self):

        rows = self.driver.find_elements(
            By.XPATH,
            "//table[@id='crudTable']/tbody/tr"
        )

        for row in rows:

            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) < 4:
                continue

            category_name = cells[1].text.strip()
            status = cells[3].text.strip()

            if status.lower() == "active":
                return category_name

        raise Exception("No active category found")

    def get_first_active_category_and_manufacturer(self):

        rows = self.driver.find_elements(
            By.XPATH,
            "//table[@id='crudTable']/tbody/tr"
        )

        for row in rows:

            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) < 4:
                continue

            category_name = cells[1].text.strip()
            manufacturer_name = cells[2].text.strip()
            status = cells[3].text.strip()

            print(
                f"Category={category_name} | "
                f"Manufacturer={manufacturer_name} | "
                f"Status={status}"
            )

            if status.lower() == "active":
                return (
                    manufacturer_name,
                    category_name
                )

        raise Exception(
            "No Active Category Found"
        )

    def get_first_category_name(self):
        return self.get_text(self.FIRST_ROW_CATEGORY).strip()

    def get_first_status(self):
        return self.get_text(self.FIRST_ROW_STATUS).strip()