import pytest
import time
from selenium.webdriver.common.by import By

from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.User_Management.Users.user_filters import user_filters
from pages.QR_monitering.QR_code_monitering import QR_code_monitering_page
from utilities.customlogger import LogGen
from utilities.readproperties import Readconfig
from utilities.read_excel import get_test_data
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------
# LOAD EXCEL DATA
# ---------------------------
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "user_filters")

@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
class Test_UM_user_filters(BaseTest):

    logger = LogGen.loggen()

    def test_user_filters(self, driver, data):

        search_name = data["search_name"]
        select_status = data["select_status"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        self.logger.info(
            f"===== User_management_user_filters ====="
        )
        # ---------------------------

        # LOGIN (ONLY ONCE)
        # ---------------------------
        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()

            self.logger.info("Login successful (first iteration)")
        else:
            self.logger.info("Skipping login — already logged in")

        # ---------------------------
        # NAVIGATION
        # ---------------------------
        UM_user_filters = user_filters(driver)
        UM_user_filters.Click_Dashboard()
        UM_user_filters.Click_User_management()
        UM_user_filters.Click_users()
        UM_user_filters.Enter_search_field(search_name)
        UM_user_filters.Choose_select_status(select_status)
        UM_user_filters.Click_filter_calender()
        UM_user_filters.select_date_range(start_date,end_date)

        status =UM_user_filters.search_product(search_name)  # True if rows exist

        if not status:
            take_screenshot(
                driver,
                test_name="user_filter_failed",
                folder_name="Screenshots\\User_Management\\Users\\filter"
            )
            self.logger.error("Roles and permission , Filter applied but no records found in table")
            assert status, "No rows found after applying filters!"
        self.logger.info("Filter applied successfully, table has records")
        time.sleep(2)

        UM_user_filters.Click_actions_icon()
        #
        try:
            UM_user_filters.Click_suspend_opt()
            UM_user_filters.Click_suspend_btn()
            time.sleep(2)

        except:
            UM_user_filters.Click_activate_opt()
            UM_user_filters.Click_Activate_btn()
            time.sleep(2)






