import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class SAEnquiryAssignPage(BasePage):

    # ---------------- TABLE ----------------

    ACTION_DOTS = (
        By.XPATH,
        "//table//tbody/tr[1]//button[@data-bs-toggle='dropdown']"
    )

    ASSIGNED_USER_COLUMN = (
        By.XPATH,
        "//table//tbody/tr[1]/td[6]"
    )

    # ---------------- MENU OPTIONS ----------------

    ASSIGN_INTERNAL_USER = (
        By.XPATH,
        "//button[contains(normalize-space(),'Assign Internal User')]"
    )

    UNASSIGN_INTERNAL_USER = (
        By.XPATH,
        "//button[contains(normalize-space(),'Un-assign Internal User')]"
    )

    # ---------------- ASSIGN POPUP ----------------

    SELECT2_DROPDOWN = (
        By.XPATH,
        "//span[contains(@class,'select2-selection')]"
    )

    SELECT2_SEARCH = (
        By.XPATH,
        "//input[@type='search']"
    )

    SELECTED_USER_TEXT = (
        By.XPATH,
        "//span[contains(@id,'select2-assigned_to-container')]"
    )

    SUBMIT_BTN = (
        By.XPATH,
        "//button[normalize-space()='Submit']"
    )

    ASSIGN_SUCCESS_OK = (
        By.XPATH,
        "//button[normalize-space()='OK']"
    )

    ASSIGN_USER_DROPDOWN = (
        By.XPATH,
        "//div[@id='assignInternalUserModal']//span[contains(@class,'select2-selection--single')]"
    )

    SELECTED_USER = (
        By.XPATH,
        "//span[contains(@id,'select2-assigned_to-container')]"
    )

    SUBMIT_BTN = (
        By.XPATH,
        "//button[normalize-space()='Submit']"
    )

    SUCCESS_OK = (
        By.XPATH,
        "//button[normalize-space()='OK']"
    )

    # ---------------- UNASSIGN ----------------

    UNASSIGN_YES = (
        By.XPATH,
        "//button[contains(.,'Yes, un-assign')]"
    )

    UNASSIGN_SUCCESS_OK = (
        By.XPATH,
        "//button[normalize-space()='OK']"
    )

    # =====================================================

    def open_actions(self):

        btn = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.presence_of_element_located(
                self.ACTION_DOTS
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            btn
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        time.sleep(3)

        print("===== DROPDOWN HTML =====")

        try:
            dropdown = self.driver.find_element(
                By.XPATH,
                "//ul[contains(@class,'dropdown-menu')]"
            )

            print(dropdown.get_attribute("outerHTML"))

        except Exception as e:
            print("Dropdown not found:", e)
    # =====================================================

    def assign_option_visible(self):

        return len(
            self.driver.find_elements(
                *self.ASSIGN_INTERNAL_USER
            )
        ) > 0

    def unassign_option_visible(self):

        return len(
            self.driver.find_elements(
                *self.UNASSIGN_INTERNAL_USER
            )
        ) > 0

    # =====================================================

    def assign_first_internal_user(self):

        # Click Assign Internal User
        self.open_actions()

        time.sleep(1)

        time.sleep(1)

        assign_btn = self.driver.find_element(
            By.XPATH,
            "//button[contains(normalize-space(),'Assign Internal User')]"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            assign_btn
        )


        print("Assign Internal User clicked")

        # Wait modal
        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    "assignInternalUserModal"
                )
            )
        )

        print("Assign modal opened")

        # Internal User dropdown
        dropdown = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@id='assignInternalUserModal']//span[contains(@class,'select2-selection--single')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )

        time.sleep(1)

        dropdown.click()

        print("Dropdown clicked")

        time.sleep(2)

        # Search box appears after dropdown opens
        search_box = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[@class='select2-search__field']"
                )
            )
        )

        print("Search box visible")

        # Select first user
        search_box.send_keys(Keys.HOME)

        time.sleep(1)

        search_box.send_keys(Keys.ENTER)

        print("User selected")

        time.sleep(2)

        selected_user = self.get_text(
            self.SELECTED_USER
        ).strip()

        print(f"Selected User = {selected_user}")

        self.click(
            self.SUBMIT_BTN
        )

        time.sleep(2)

        try:
            self.click(
                self.SUCCESS_OK
            )
        except:
            pass

        return selected_user
    # =====================================================

    def unassign_internal_user(self):

        self.open_actions()

        self.click(
            self.UNASSIGN_INTERNAL_USER
        )

        self.click(
            self.UNASSIGN_YES
        )

        self.click(
            self.UNASSIGN_SUCCESS_OK
        )

        WebDriverWait(
            self.driver,
            20
        ).until(
            lambda d:
            self.get_first_row_assigned_user()
            == "Not Assigned"
        )

    # =====================================================

    def get_first_row_assigned_user(self):

        return self.get_text(
            self.ASSIGNED_USER_COLUMN
        ).strip()

    def is_first_row_assigned(self):

        value = self.get_first_row_assigned_user().strip()

        return value.lower() != "not assigned"

    def ensure_user_assigned(self):

        if self.is_first_row_assigned():
            print("Already assigned")

            return self.get_first_row_assigned_user()

        return self.assign_first_internal_user()

    def ensure_user_unassigned(self):

        if not self.is_first_row_assigned():
            print("Already unassigned")

            return

        self.unassign_internal_user()