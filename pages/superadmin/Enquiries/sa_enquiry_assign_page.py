from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


class SAEnquiryAssignPage(BasePage):

    # ----------------- ACTION (3 DOTS) -----------------
    ACTION_DOTS = (
        By.XPATH,
        "//table[contains(@class,'dataTable')]//tbody/tr[1]//button[@data-bs-toggle='dropdown']"
    )

    DROPDOWN_MENU_OPEN = (
        By.XPATH,
        "//ul[contains(@class,'dropdown-menu') and contains(@class,'show')]"
    )

    # ----------------- ASSIGN INTERNAL USER -----------------
    ASSIGN_BTN = (
        By.XPATH,
        "//table/tbody/tr[1]//button[normalize-space()='Assign Internal User']"
    )

    INTERNAL_USER_DROPDOWN = (By.ID, "assigned_to")
    SUBMIT_ASSIGN = (By.XPATH, "//button[contains(text(),'Submit')]")

    ASSIGN_SUCCESS_MSG = (
        By.XPATH,
        "//div[@class='swal2-html-container' and contains(text(),'Internal user assigned successfully')]"
    )
    ASSIGN_SUCCESS_OK = (By.XPATH, "//button[normalize-space()='OK']")

    # ----------------- UNASSIGN -----------------
    UNASSIGN_BTN = (
        By.XPATH,
        "//button[normalize-space()='Un-assign Internal User']"
    )

    UNASSIGN_CONFIRM_CANCEL = (
        By.XPATH,
        "//button[normalize-space()='No, cancel']"
    )
    UNASSIGN_CONFIRM_YES = (
        By.XPATH,
        "//button[normalize-space()='Yes, un-assign']"
    )

    UNASSIGN_SUCCESS_POPUP = (
        By.XPATH,
        "//div[normalize-space()='Internal user un-assigned successfully.']"
    )
    UNASSIGN_SUCCESS_OK = (By.XPATH, "//button[normalize-space()='OK']")

    # ----------------- TABLE COLUMN -----------------
    ASSIGNED_USER_COLUMN = (
        By.XPATH,
        "//table//tbody/tr[1]/td[6]//span"
    )

    # ================= ACTION METHODS =================

    def open_actions(self, retries=3):
        """
        Always re-locate the action button to avoid stale element issues.
        """
        for attempt in range(retries):
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.ACTION_DOTS)
                )
                self.click(self.ACTION_DOTS)

                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(self.DROPDOWN_MENU_OPEN)
                )
                return

            except StaleElementReferenceException:
                if attempt == retries - 1:
                    raise

    def open_assign_user(self):
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.ASSIGN_BTN)
        )
        self.click(self.ASSIGN_BTN)

    def choose_internal_user(self, name):
        """Select internal user from dropdown"""
        dropdown = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.INTERNAL_USER_DROPDOWN)
        )
        Select(dropdown).select_by_visible_text(name)

    def submit_assign_user(self):
        self.click(self.SUBMIT_ASSIGN)

    def confirm_assign_success(self):
        """Confirm success popup after assigning internal user"""
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.ASSIGN_SUCCESS_MSG)
        )
        self.click(self.ASSIGN_SUCCESS_OK)

        # Wait for popup to disappear before touching table
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.ASSIGN_SUCCESS_MSG)
        )

    # ================= TABLE VALUE (CRITICAL FIX) =================

    def assigned_user_value(self, timeout=15):
        """Stable read of Assigned User column (handles DataTable refresh)"""
        def _get_value(driver):
            try:
                el = driver.find_element(*self.ASSIGNED_USER_COLUMN)
                text = el.text.strip()
                return text if text else False
            except:
                return False

        return WebDriverWait(self.driver, timeout).until(_get_value)

    # ================= UNASSIGN ACTIONS =================

    def click_unassign(self):
        if not self.is_element_visible(self.UNASSIGN_BTN):
            return False

        self.click(self.UNASSIGN_BTN)
        return True

    def confirm_unassign_yes(self):
        self.click(self.UNASSIGN_CONFIRM_YES)

    def confirm_unassign_cancel(self):
        self.click(self.UNASSIGN_CONFIRM_CANCEL)

    def confirm_unassign_success(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.UNASSIGN_SUCCESS_POPUP)
        )
        self.click(self.UNASSIGN_SUCCESS_OK)

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.UNASSIGN_SUCCESS_POPUP)
        )

    def wait_until_unassigned(self):
        WebDriverWait(self.driver, 15).until(
            lambda d: self.assigned_user_value() == "Not Assigned"
        )

    # ================= STATE SAFE METHOD =================

    def ensure_user_assigned(self, name="Sunio Soni"):
        """Ensures user is assigned before test continues"""
        current = self.assigned_user_value()

        if current != name:
            self.open_actions()
            self.open_assign_user()
            self.choose_internal_user(name)
            self.submit_assign_user()
            self.confirm_assign_success()

            WebDriverWait(self.driver, 15).until(
                lambda d: self.assigned_user_value() == name
            )

    def wait_for_table_refresh(self):
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//table//tbody/tr[1]/td[6]//span")
                )
            )
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//table//tbody/tr[1]/td[6]//span")
                )
            )
