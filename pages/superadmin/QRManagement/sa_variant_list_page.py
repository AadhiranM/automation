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

    CREATE_BTN = (
        By.XPATH,
        "//a[normalize-space()='Create Variants']"
    )

    def click_create(self):
        self.click(self.CREATE_BTN)
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
        self.wait_for_table()   #  avoid stale

    def click_previous(self):
        self.click(self.PREV_BTN)
        self.wait_for_table()   #  avoid stale

    # =============================
    # ACTIONS (GENERIC + FINAL)
    # =============================
    def click_actions_with_option(self, require_view=False, require_edit=False):
        rows = self.driver.find_elements(*self.TABLE_ROWS)

        for i in range(len(rows)):
            locator = (By.XPATH, self.ACTION_BTN.format(i + 1))
            self.click(locator)

            # wait dropdown
            WebDriverWait(self.driver, 15).until(
                lambda d:
                d.find_elements(*self.VIEW_BTN)
                or d.find_elements(*self.EDIT_BTN)
            )

            view_present = len(self.driver.find_elements(*self.VIEW_BTN)) > 0
            edit_present = len(self.driver.find_elements(*self.EDIT_BTN)) > 0

            # LOGIC
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

            # not matching → close dropdown and try next
            self.driver.execute_script("document.body.click()")

        raise Exception("No matching row found for required actions")

    def click_view(self):

        view = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.VIEW_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            view
        )

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.VIEW_BTN)
        )

        try:
            view.click()
        except:
            self.driver.execute_script(
                "arguments[0].click();",
                view
            )

    def click_edit(self):

        edit = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.EDIT_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            edit
        )

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.EDIT_BTN)
        )

        try:
            edit.click()
        except:
            self.driver.execute_script(
                "arguments[0].click();",
                edit
            )

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

    def is_category_present(self, category_name):

        rows = self.driver.find_elements(*self.TABLE_ROWS)

        for row in rows:

            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) >= 2:

                category = cells[1].text.strip()

                if category.lower() == category_name.lower():
                    return True

        return False

    def is_created_by_present(self, username):

        print(f"Expected Username : {username}")

        rows = self.driver.find_elements(*self.TABLE_ROWS)

        for row in rows:

            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) >= 4:

                created_by = cells[3].text.strip()

                print(f"Created By : {created_by}")

                if username is not None and username.lower() in created_by.lower():
                    return True

        return False

    def wait_for_table_refresh(self):

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                self.TABLE_ROWS
            )
        )

    def is_variant_value_present(self, value):

        rows = self.driver.find_elements(
            *self.TABLE_ROWS
        )

        for row in rows:

            if value.lower() in row.text.lower():
                return True

        return False

    def get_first_variant_type(self):

        rows = self.driver.find_elements(*self.TABLE_ROWS)

        for row in rows:

            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) >= 3:

                variant_type = cells[2].text.strip()

                if (
                        variant_type
                        and "No Variants" not in variant_type
                ):
                    return variant_type

        raise Exception("No Variant Type found")

    def get_first_manufacturer_name(self):

        rows = self.driver.find_elements(*self.TABLE_ROWS)

        for row in rows:

            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) >= 1:

                manufacturer = cells[0].text.strip()

                if manufacturer:
                    return manufacturer

        raise Exception("No Manufacturer found")
