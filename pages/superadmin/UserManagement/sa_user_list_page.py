from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.common.base_page import BasePage
import time


class SAUserListPage(BasePage):

    # =====================================================
    # SEARCH
    # =====================================================

    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    # =====================================================
    # STATUS FILTER
    # =====================================================

    STATUS_DROPDOWN = (
        By.XPATH,
        "//span[contains(@class,'selection')]//span[contains(text(),'Select Status')]"
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

    FIRST_ROW_NAME = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    FIRST_MANUFACTURER = (
        By.XPATH,
        "//table/tbody/tr[1]/td[3]"
    )

    FIRST_USERS = (
        By.XPATH,
        "//table/tbody/tr[1]/td[4]"
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

    PAGE_NUMBER = "//a[normalize-space()='{}']"

    # =====================================================
    # PAGE LOAD
    # =====================================================

    VIEW_OPTION = (
        By.XPATH,
        "//ul[contains(@class,'show')]//a[contains(@href,'/show')]"
    )

    EDIT_MOBILE_INPUT = (
        By.XPATH,
        "//input[@name='mobile']"
    )

    FIRST_ROW_THREE_DOTS = (
        By.XPATH,
        "//table[@id='crudTable']/tbody/tr[1]/td[last()]//button[contains(@class,'dropdown')]"
    )

    EDIT_OPTION = (
        By.XPATH,
        "//ul[contains(@class,'dropdown-menu') and contains(@class,'show')]//button[contains(@class,'edit-report-btn')]"
    )

    EDIT_NAME_INPUT = (
        By.NAME,
        "name"
    )
    UPDATE_BTN = (
        By.XPATH,
        "//button[contains(text(),'Submit')]"
    )

    ROLE_PERMISSION_OPTION = (
        By.XPATH,
        "//a[contains(.,'Role & Permissions')]"
    )

    SUSPEND_OPTION = (
        By.XPATH,
        "//a[contains(.,'Suspend')] | //button[contains(.,'Suspend')] | //li[contains(.,'Suspend')]"
    )

    ACTIVATE_OPTION = (
        By.XPATH,
        "//a[contains(.,'Activate')]"
    )

    CONFIRM_SUSPEND_BTN = (
        By.XPATH,
        "//button[contains(text(),'Suspend')]"
    )

    CONFIRM_ACTIVATE_BTN = (
        By.XPATH,
        "//button[contains(text(),'Activate')]"
    )

    FIRST_ROW_STATUS = (
        By.XPATH,
        "(//td[contains(@class,'sorting_1')]/following-sibling::td//span)[1]"
    )

    FIRST_ROW_ACTIVE_STATUS = (
        By.XPATH,
        "//table/tbody/tr[1]//span[contains(text(),'Active')]"
    )

    FIRST_ROW_SUSPENDED_STATUS = (
        By.XPATH,
        "//table/tbody/tr[1]//span[contains(text(),'Suspended')]"
    )
    def goto_page(self):

        self.driver.get(
            "https://beta.digitathya.com/admin/user?reset_filters=1"
        )

        self.wait_for_results()

    def get_first_manufacturer(self):
        return self.get_text(
            self.FIRST_MANUFACTURER
        ).strip()

    def get_first_users_count(self):
        return self.get_text(
            self.FIRST_USERS
        ).strip()

    # =====================================================
    # WAIT
    # =====================================================
    def open_first_row_actions(self):

        self.safe_click(self.FIRST_ROW_THREE_DOTS)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//ul[contains(@class,'dd_action') and contains(@class,'show')]"
            ))
        )

    def click_three_dots(self):

        self.safe_click(self.FIRST_ROW_THREE_DOTS)

        time.sleep(2)

    def click_suspend(self):

        time.sleep(2)

        suspend_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.SUSPEND_OPTION
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            suspend_btn
        )

        time.sleep(2)

    def click_status_action(self):

        self.click_three_dots()

        time.sleep(2)

        try:
            suspend = self.driver.find_element(
                By.XPATH,
                "//*[contains(text(),'Suspend')]"
            )

            suspend.click()

            return "Suspended"

        except:

            activate = self.driver.find_element(
                By.XPATH,
                "//*[contains(text(),'Activate')]"
            )

            activate.click()

            return "Active"
    def confirm_suspend(self):

        self.safe_click(self.CONFIRM_SUSPEND_BTN)

        time.sleep(5)

    def click_activate(self):

        # Re-open dropdown
        self.click_three_dots()

        activate_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//a[contains(.,'Activate')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            activate_btn
        )

        time.sleep(2)

    def click_view(self):

        self.open_first_row_actions()

        wait = WebDriverWait(self.driver, 10)

        view = wait.until(
            EC.visibility_of_element_located(self.VIEW_OPTION)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            view
        )

        wait.until(
            lambda d: "/show" in d.current_url
        )

        print(self.driver.current_url)

    def click_edit(self):
        # Open 3 dots menu
        self.safe_click(self.FIRST_ROW_THREE_DOTS)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//a[contains(.,'Edit')]"
            ))
        )

        time.sleep(2)

        # Click Edit using direct xpath
        edit_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//a[contains(.,'Edit')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            edit_btn
        )

        time.sleep(3)

    def suspend_user(self):
        self.open_first_row_actions()

        # Click Suspend option
        self.safe_click(self.SUSPEND_OPTION)

        # Wait until confirm button is clickable
        confirm_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.CONFIRM_SUSPEND_BTN)
        )

        # Click confirm
        self.driver.execute_script("arguments[0].click();", confirm_btn)

        # Wait until popup disappears
        WebDriverWait(self.driver, 20).until(
            EC.invisibility_of_element_located(self.CONFIRM_SUSPEND_BTN)
        )

        self.wait_for_results()

    def activate_user(self):
        self.open_first_row_actions()

        self.safe_click(self.ACTIVATE_OPTION)

        time.sleep(2)

        self.safe_click(self.CONFIRM_ACTIVATE_BTN)

        time.sleep(4)

    def is_element_present(self, locator):

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(locator)
            )
            return True

        except:
            return False

    def get_first_row_status(self):

        time.sleep(4)

        if self.is_element_present(self.FIRST_ROW_ACTIVE_STATUS):
            return "Active"

        elif self.is_element_present(self.FIRST_ROW_SUSPENDED_STATUS):
            return "Suspended"

        return "Unknown"

    def click_role_permissions(self):

        wait = WebDriverWait(self.driver, 20)

        # Open 3 dots menu for current searched row
        self.click_three_dots()

        # Wait for Role & Permissions option
        role_btn = wait.until(
            EC.visibility_of_element_located(
                self.ROLE_PERMISSION_OPTION
            )
        )

        # Scroll option into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            role_btn
        )

        # JS click because dropdown menu can have
        # overlay/interception issues in parallel execution
        self.driver.execute_script(
            "arguments[0].click();",
            role_btn
        )

        # Wait until navigation actually happens
        wait.until(
            EC.url_contains("permission")
        )
    def wait_for_results(self):

        WebDriverWait(self.driver, 15).until(
            lambda d:
            d.find_elements(*self.FIRST_ROW)
            or
            d.find_elements(*self.NO_DATA)
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_first_user(self):

        user_name = self.get_text(
            self.FIRST_ROW_NAME
        ).strip()

        self.type(
            self.SEARCH_BOX,
            user_name
        )

        self.click(self.SEARCH_BTN)

        self.wait_for_results()

        return user_name

    # =====================================================
    # STATUS FILTER
    # =====================================================

    def filter_by_status(self, status):

        wait = WebDriverWait(self.driver, 30)

        print(f"Selecting status = {status}")

        dropdown = wait.until(
            EC.presence_of_element_located(
                self.STATUS_DROPDOWN
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )

        time.sleep(1)

        ActionChains(self.driver)\
            .move_to_element(dropdown)\
            .click()\
            .perform()

        print("Status dropdown clicked")

        time.sleep(2)

        option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//li[contains(text(),'{status}')]"
            ))
        )

        ActionChains(self.driver)\
            .move_to_element(option)\
            .click()\
            .perform()

        print(f"Selected status = {status}")

        time.sleep(3)

        self.wait_for_results()

    # =====================================================
    # ENTRIES
    # =====================================================

    def set_entries_per_page(self, value):

        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                self.ENTRIES_DROPDOWN
            )
        )

        Select(dropdown).select_by_value(str(value))

        self.wait_for_results()

    # =====================================================
    # PAGINATION
    # =====================================================

    def click_next(self):

        next_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.NEXT_BTN
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            next_btn
        )

        self.wait_for_results()

    def click_previous(self):

        prev_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.PREVIOUS_BTN
            )
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

    # =====================================================
    # VALIDATIONS
    # =====================================================

    def is_row_present(self):

        return len(
            self.driver.find_elements(*self.FIRST_ROW)
        ) > 0

    def has_no_data(self):

        return len(
            self.driver.find_elements(*self.NO_DATA)
        ) > 0

    def search_user(self, user_name):

        wait = WebDriverWait(self.driver, 30)

        # Enter updated user name
        self.type(self.SEARCH_BOX, user_name)

        # Click Search
        self.safe_click(self.SEARCH_BTN)

        # Wait until the searched user appears in the result
        wait.until(
            lambda d: self.get_first_row_name() == user_name
        )

    def get_first_row_name(self):
        return self.get_text(
            self.FIRST_ROW_NAME
        ).strip()

    def update_user_details(self, new_name, new_mobile):

        wait = WebDriverWait(self.driver, 20)

        # Update Name
        name_field = wait.until(
            EC.visibility_of_element_located(
                self.EDIT_NAME_INPUT
            )
        )

        name_field.clear()
        name_field.send_keys(new_name)

        # Update Mobile
        mobile_field = wait.until(
            EC.visibility_of_element_located(
                self.EDIT_MOBILE_INPUT
            )
        )

        mobile_field.clear()
        mobile_field.send_keys(new_mobile)

        # Click Update / Submit
        self.safe_click(self.UPDATE_BTN)

        # Wait until redirected from Edit page
        wait.until(
            lambda d: "edit" not in d.current_url.lower()
        )

        print(f"User name updated: {new_name}")
        print(f"User mobile updated: {new_mobile}")

    # =====================================================
    # DATE FILTER
    # =====================================================

    def filter_by_date(self, start, end):

        wait = WebDriverWait(
            self.driver,
            15
        )

        print(
            f"Selecting date range: "
            f"{start.strftime('%d %b %Y')} - "
            f"{end.strftime('%d %b %Y')}"
        )

        # -------------------------------------------------
        # Open Created At date picker
        # -------------------------------------------------

        date_filter = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[@placeholder='Filter by : Created At']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            date_filter
        )

        self.driver.execute_script(
            "arguments[0].click();",
            date_filter
        )

        print("Date picker opened")

        # -------------------------------------------------
        # Get current calendar year
        # -------------------------------------------------

        year_input = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'flatpickr-calendar') "
                    "and contains(@class,'open')]"
                    "//input[contains(@class,'numInput')]"
                )
            )
        )

        current_year = int(
            year_input.get_attribute("value")
        )

        target_year = start.year

        print(
            f"Current calendar year: {current_year}"
        )

        print(
            f"Target year: {target_year}"
        )

        # -------------------------------------------------
        # YEAR DOWN ARROW
        #
        # Example:
        # 2026 -> 2025 -> 2024
        # -------------------------------------------------

        while current_year > target_year:
            year_down = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[contains(@class,'flatpickr-calendar') "
                        "and contains(@class,'open')]"
                        "//span[contains(@class,'arrowDown')]"
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                year_down
            )

            self.driver.execute_script(
                "arguments[0].click();",
                year_down
            )

            time.sleep(0.5)

            year_input = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class,'flatpickr-calendar') "
                        "and contains(@class,'open')]"
                        "//input[contains(@class,'numInput')]"
                    )
                )
            )

            current_year = int(
                year_input.get_attribute("value")
            )

            print(
                f"Year after DOWN arrow: {current_year}"
            )

        # -------------------------------------------------
        # Verify target year
        # -------------------------------------------------

        assert current_year == target_year, (
            f"Year navigation failed. "
            f"Expected {target_year}, "
            f"Actual {current_year}"
        )

        print(
            f"Year successfully changed to {target_year}"
        )

        # -------------------------------------------------
        # Change month using MONTH DROPDOWN
        #
        # Example:
        # September 2024 -> January 2024
        # -------------------------------------------------

        month_dropdown = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'flatpickr-calendar') "
                    "and contains(@class,'open')]"
                    "//select[contains("
                    "@class,"
                    "'flatpickr-monthDropdown-months'"
                    ")]"
                )
            )
        )

        Select(
            month_dropdown
        ).select_by_visible_text(
            start.strftime("%B")
        )

        print(
            f"Month changed to {start.strftime('%B')}"
        )

        # -------------------------------------------------
        # Select START DATE
        # -------------------------------------------------

        start_date = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'flatpickr-calendar') "
                    "and contains(@class,'open')]"
                    f"//span[contains(@class,'flatpickr-day') "
                    f"and @aria-label='{start.strftime('%B %-d, %Y')}']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            start_date
        )

        print(
            f"Selected start date: "
            f"{start.strftime('%d %b %Y')}"
        )

        # -------------------------------------------------
        # Select END DATE
        # -------------------------------------------------

        end_date = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'flatpickr-calendar') "
                    "and contains(@class,'open')]"
                    f"//span[contains(@class,'flatpickr-day') "
                    f"and @aria-label='{end.strftime('%B %-d, %Y')}']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            end_date
        )

        print(
            f"Selected end date: "
            f"{end.strftime('%d %b %Y')}"
        )

        # -------------------------------------------------
        # Click Filter button
        # -------------------------------------------------

        filter_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[normalize-space()='Filter']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            filter_button
        )

        print("Filter button clicked")

        # -------------------------------------------------
        # Wait for result / no-result state
        # -------------------------------------------------

        self.wait_for_results()

        print(
            "Date filter completed successfully"
        )