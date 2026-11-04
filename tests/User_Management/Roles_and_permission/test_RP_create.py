import pytest
import time
import random
import string

from selenium.webdriver.common.by import By
from pages.User_Management.Roles_and_Permission.create import Roles_and_permission_create
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.mark.order(1)
class Test_UM_RP_create(BaseTest):

    logger = LogGen.loggen()

    def test_Roles_and_permission_create(self, driver):

        # =========================
        # DYNAMIC TEST DATA
        # =========================
        Role_name = random.choice(string.ascii_uppercase) + ''.join(
            random.choices(string.ascii_lowercase, k=4)
        )

        User_type = "Manufacturer"  # Change according to your application
        select_status = "Active"

        self.logger.info(
            f"===== START TEST | Roles_and_permission_create | ROLE={Role_name} ====="
        )

        # =========================
        # ACTION FLOW
        # =========================
        UM_roles_and_per = Roles_and_permission_create(driver)

        self.logger.info("Navigating to Dashboard")
        UM_roles_and_per.Click_Dashboard()

        self.logger.info("Opening User Management module")
        UM_roles_and_per.Click_User_management()

        self.logger.info("Opening Roles & Permission page")
        UM_roles_and_per.Click_roles_and_permission()

        self.logger.info("Opening Create Role form")
        UM_roles_and_per.Click_create()

        self.logger.info(f"Entering generated Role Name: {Role_name}")
        UM_roles_and_per.Enter_role_name(Role_name)

        self.logger.info(f"Selecting User Type: {User_type}")
        UM_roles_and_per.select_user_type(User_type)

        self.logger.info("Selecting Status: Active")
        UM_roles_and_per.select_status(select_status)

        self.logger.info("Selecting Check All permissions")
        UM_roles_and_per.select_check_all_btn()

        # =========================
        # SUBMIT
        # =========================
        self.logger.info("Submitting Role Creation form")
        UM_roles_and_per.Click_submit_btn()

        # =========================
        # TOAST VALIDATION
        # =========================
        self.logger.info("Waiting for Role Creation toast")

        try:
            toast_text = WebDriverWait(driver,20).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".toastify")
                )
            ).text.strip()
            toast_text = toast_text.encode("ascii", errors="ignore").decode()
            print("Toast:", toast_text)

            self.logger.info(f"Toast received: {toast_text}")

        except TimeoutException:
            toast_text = "Toast message not displayed"

            print("Toast:", toast_text)

            self.logger.error(
                "Role creation toast message not displayed"
            )

        # =========================
        # RESULT
        # =========================
        if "Role created successfully" in toast_text:

            self.logger.info(
                f"Role created successfully | Role Name: {Role_name} | {toast_text}"
            )

        else:

            self.logger.error(
                f"Role creation failed | Role Name: {Role_name} | Toast: {toast_text}"
            )

            take_screenshot(
                driver,
                test_name="UM_Role_create_fail",
                folder_name="Screenshots\\User_Management\\Roles_and_permission"
            )

            assert False, (
                f"Role creation failed | Role Name: {Role_name} | Toast: {toast_text}"
            )

        self.logger.info(
            "===== Roles_and_permission_create Test Completed Successfully ====="
        )