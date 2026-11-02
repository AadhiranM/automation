
import pytest
import random
import string

from selenium.webdriver.common.by import By
from pages.User_Management.Users.user_create import user_create
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.mark.order(1)
class Test_UM_users_create(BaseTest):

    logger = LogGen.loggen()

    def test_users_create(self, driver):

        # =========================
        # GENERATE DYNAMIC USER DATA
        # =========================

        # Username contains alphabets only
        user_name = ''.join(
            random.choices(string.ascii_letters, k=8)
        )

        # Dynamic email ID
        Email = (
            ''.join(random.choices(string.ascii_lowercase, k=8))
            + str(random.randint(1000, 9999))
            + "@example.com"
        )

        # Dynamic 10-digit mobile number
        Mobile_number = str(random.randint(6000000000, 9999999999))

        # Dynamic password
        password = (
            random.choice(string.ascii_uppercase)
            + random.choice(string.ascii_lowercase)
            + random.choice(string.digits)
            + random.choice("!@#$")
            + ''.join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )
        )

        select_status = "Active"
        select_Role = "User"

        # =========================
        # LOGGER START
        # =========================

        self.logger.info(
            f"===== User Management , User Creation Test Started | "
            f"Username: {user_name} ====="
        )

        self.logger.info(
            f"Generated User Details | Username: {user_name} | "
            f"Email: {Email} | Mobile: {Mobile_number} | "
            f"Status: {select_status} | Role: {select_Role}"
        )

        # =========================
        # NAVIGATION
        # =========================

        UM_create = user_create(driver)

        driver.refresh()
        self.logger.info("Page refreshed successfully")

        UM_create.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        UM_create.Click_User_management()
        self.logger.info("Opened User Management module")

        UM_create.Click_users()
        self.logger.info("Opened Users page")

        UM_create.Click_create()
        self.logger.info("Opened Create User form")

        # =========================
        # ENTER USER DETAILS
        # =========================

        UM_create.Enter_username(user_name)
        self.logger.info(f"Entered Username: {user_name}")

        UM_create.Enter_Email(Email)
        self.logger.info(f"Entered Email: {Email}")

        UM_create.select_Role_drpdown()
        UM_create.Enter_Role_input(select_Role)
        self.logger.info(f"Selected Role: {select_Role}")

        UM_create.Choose_select_status(select_status)
        self.logger.info(f"Selected Status: {select_status}")

        UM_create.Enter_Mobile_number(Mobile_number)
        self.logger.info(f"Entered Mobile Number: {Mobile_number}")

        UM_create.Enter_password(password)
        self.logger.info("Entered generated password")

        # =========================
        # SUBMIT FORM
        # =========================

        UM_create.Click_submit_btn()
        self.logger.info("Submitted user creation form")

        # =========================
        # POSITIVE VALIDATION
        # =========================

        self.logger.info("Waiting for success toast")

        try:
            toast_text = WebDriverWait(driver,30).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".toastify")
                )
            ).text.strip()

            toast_text = toast_text.encode("ascii", errors="ignore").decode()
            print("Toast:", toast_text)

            self.logger.info(f"Toast received: {toast_text}")

        except TimeoutException:
            take_screenshot(
                driver,
                test_name="UM_user_create_fail",
                folder_name="Screenshots\\User_Management\\Users\\create"
            )
            self.logger.error("Success toast did not appear")
            raise AssertionError(
                " user creation test failed: success toast not displayed"
            )

        assert "User created successfully" in toast_text, (
            f"Unexpected toast message: {toast_text}"
        )

        self.logger.info(
            f"User created successfully | Username: {user_name} | "
            f"Email: {Email}"
        )

        self.logger.info(
            "===== User Management , User Creation Test PASSED ====="
        )
