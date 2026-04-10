from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class SAVariantListPage(BasePage):

    # ===== SEARCH =====
    SEARCH_BOX = (By.XPATH, "//input[contains(@placeholder,'Search')]")
    SEARCH_BTN = (By.XPATH, "//button[contains(@class,'search')]")
    REFRESH_BUTTON = (By.XPATH, "//button[contains(@class,'refresh')]")

    # ===== TABLE =====
    TABLE_ROWS = (By.XPATH, "//table//tbody//tr")
    NO_DATA = (By.XPATH, "//td[contains(@class,'dataTables_empty')]")

    # ===== PAGINATION =====
    NEXT_BTN = (By.XPATH, "//a[text()='Next']")
    PREV_BTN = (By.XPATH, "//a[text()='Previous']")

    # ===== ACTIONS =====
    ACTION_BTN = "//table//tbody//tr[{}]//button"
    VIEW_BTN = (By.XPATH, "//a[normalize-space()='View']")
    EDIT_BTN = (By.XPATH, "//a[normalize-space()='Edit']")

    # ===== DROPDOWN =====
    ENTRIES_DROPDOWN = (By.XPATH, "//select[@name='crudTable_length']")

    # =============================
    # BASIC
    # =============================
    def goto_page(self):
        self.driver.get("https://beta.digitathya.com/admin/variant?reset_filters=1")

    def wait_for_table(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(*self.TABLE_ROWS)) > 0
        )

    # =============================
    # SEARCH
    # =============================
    def search(self, text):
        self.type(self.SEARCH_BOX, text)
        self.click(self.SEARCH_BTN)
        self.wait_for_table()   # ✅ important

    def is_no_result_displayed(self):
        return len(self.driver.find_elements(*self.NO_DATA)) > 0

    def click_refresh(self):
        self.click(self.REFRESH_BUTTON)

        # ✅ stronger wait (handles refresh properly)
        WebDriverWait(self.driver, 5).until(
            lambda d: len(d.find_elements(*self.TABLE_ROWS)) > 0
        )

    # =============================
    # PAGINATION
    # =============================
    def click_next(self):
        self.click(self.NEXT_BTN)
        self.wait_for_table()   # ✅ avoid stale

    def click_previous(self):
        self.click(self.PREV_BTN)
        self.wait_for_table()   # ✅ avoid stale

    # =============================
    # ACTIONS (GENERIC + FINAL)
    # =============================
    def click_actions_with_option(self, require_view=False, require_edit=False):
        rows = self.driver.find_elements(*self.TABLE_ROWS)

        for i in range(len(rows)):
            locator = (By.XPATH, self.ACTION_BTN.format(i + 1))
            self.click(locator)

            # wait dropdown
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.EDIT_BTN)
            )

            view_present = len(self.driver.find_elements(*self.VIEW_BTN)) > 0
            edit_present = len(self.driver.find_elements(*self.EDIT_BTN)) > 0

            # ✅ LOGIC
            if require_view and require_edit:
                if view_present and edit_present:
                    return

            elif require_view:
                if view_present:
                    return

            elif require_edit:
                if edit_present:
                    return

            else:
                # default → both required
                if view_present and edit_present:
                    return

            # ❌ not matching → close dropdown and try next
            self.driver.execute_script("document.body.click()")

        raise Exception("No matching row found for required actions")

    def click_view(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.VIEW_BTN)
        )
        self.click(self.VIEW_BTN)

    def click_edit(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.EDIT_BTN)
        )
        self.click(self.EDIT_BTN)

    # =============================
    # HELPERS
    # =============================
    def is_row_present(self):
        return len(self.driver.find_elements(*self.TABLE_ROWS)) > 0

    def set_entries_per_page(self, value):
        dropdown = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.ENTRIES_DROPDOWN)
        )
        Select(dropdown).select_by_value(str(value))

        self.wait_for_table()