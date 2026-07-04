import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.customlogger import LogGen

class Roles_and_permission_filters:
    Dashboard = (By.XPATH, "//span[@class='nav-name'][normalize-space()='Dashboard']")
    user_management_opt=(By.XPATH,"//span[normalize-space()='User Management']")
    roles_and_permission=(By.XPATH,"//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Roles & Permissions']")
    refresh_btn=(By.XPATH,"//button[contains(@class,'btn btn-outline-primary btn-icon waves-effect waves-light reload_btn uicust-active-color uicust-active-border refresh_Btn')]")
    search_name_field=(By.XPATH,"(//input[@id='search-vale'])[1]")
    filter_calender=(By.XPATH,"//input[@class='form-control dash-filter-picker active form-control input']")
    select_status=(By.XPATH,"//select[@id='idStatus']")
    actions_icon=(By.XPATH,"(//button[@type='button'])[13]")
    inactive_opt=(By.XPATH,"//ul[@class='dropdown-menu dropdown-menu-end dd_action show']//a[@class='dropdown-item status-item-btn icons-designed'][normalize-space()='Inactive']")
    active_opt=(By.XPATH,"//a[normalize-space()='Activate']")
    Activate_btn=(By.XPATH,"//button[normalize-space()='Activate']")
    Inactive_opt=(By.XPATH,"//ul[@class='dropdown-menu dropdown-menu-end dd_action show']//a[@class='dropdown-item status-item-btn icons-designed'][normalize-space()='Inactive']")
    suspend_btn=(By.XPATH,"//button[normalize-space()='Suspend']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = LogGen.loggen()

    # ================= NAVIGATION =================
    def Click_Dashboard(self):
        self.driver.find_element(*self.Dashboard).click()

    def Click_User_management(self):
        self.driver.find_element(*self.user_management_opt).click()

    def Click_roles_and_permission(self):
        self.driver.find_element(*self.roles_and_permission).click()

    def select_date_range(self, start_date, end_date):
        """
        Flatpickr range selection
        start_date / end_date → YYYY-MM-DD
        """

        start_year, start_month, start_day = start_date.split("-")
        end_year, end_month, end_day = end_date.split("-")

        start_month_name = calendar.month_name[int(start_month)]
        end_month_name = calendar.month_name[int(end_month)]

        calendar_popup = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]"

        self.wait.until(EC.visibility_of_element_located((By.XPATH, calendar_popup)))

        # START DATE
        year_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, calendar_popup + "//input[@aria-label='Year']"))
        )
        year_input.clear()
        year_input.send_keys(start_year)

        month_dropdown = Select(
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, calendar_popup + "//select[@aria-label='Month']"))
            )
        )
        month_dropdown.select_by_visible_text(start_month_name)
        time.sleep(0.5)

        for d in self.driver.find_elements(By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"):
            classes = d.get_attribute("class")
            if (
                    d.text == str(int(start_day))
                    and "flatpickr-disabled" not in classes
                    and "notAllowed" not in classes
                    and "prevMonthDay" not in classes
                    and "nextMonthDay" not in classes
            ):
                d.click()
                break

        # for d in self.driver.find_elements(By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"):
        #     if d.text == str(int(start_day)) and "disabled" not in d.get_attribute("class"):
        #         d.click()
        #         break

        time.sleep(1)

        # END DATE
        if start_year != end_year or start_month_name != end_month_name:
            year_input.clear()
            year_input.send_keys(end_year)
            month_dropdown.select_by_visible_text(end_month_name)
            time.sleep(1)

        for d in self.driver.find_elements(By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"):
            if d.text == str(int(end_day)) and "disabled" not in d.get_attribute("class"):
                d.click()
                break
        time.sleep(1)

    # def search_product(self, search_name):
    #     flag = False
    #     try:
    #         # Check if table has empty message
    #         empty_cells = self.driver.find_elements(By.XPATH, "//table[@id='crudTable']//td[@class='dataTables_empty']")
    #         if empty_cells:
    #             print("Table is empty")
    #             return False
    #
    #         # Get all rows in tbody
    #         rows = self.driver.find_elements(By.XPATH, "//table[@id='crudTable']//tbody//tr")
    #
    #         for r in range(1, len(rows) + 1):
    #             # Get product_name and batch_no using full XPath
    #             role_name = self.driver.find_element(
    #                 By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[2]"
    #             ).text.strip()
    #             active_status = self.driver.find_element(
    #                 By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[5]"
    #             ).text.strip()
    #             time.sleep(1)
    #             print(active_status)
    #             print(role_name)
    #             if search_name == role_name:
    #                 flag = True
    #                 break
    #
    #     except Exception as e:
    #         print(f"Exception in searching product: {e}")
    #         flag = False
    #
    #     return flag

    def search_product(self, search_name, expected_status=None):
        try:
            empty_cells = self.driver.find_elements(
                By.XPATH, "//table[@id='crudTable']//td[@class='dataTables_empty']"
            )
            if empty_cells:
                self.logger.warning("Table is empty")
                return False

            rows = self.driver.find_elements(
                By.XPATH, "//table[@id='crudTable']//tbody//tr"
            )

            for r in range(1, len(rows) + 1):

                role_name = self.driver.find_element(
                    By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[2]"
                ).text.strip()
                time.sleep(1)

                active_status = self.driver.find_element(
                    By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[5]"
                ).text.strip()
                time.sleep(1)

                if search_name == role_name:
                    print(f"Data found: {role_name}")
                    # Match found
                    self.logger.info(f"Product found: {role_name}")
                    if expected_status:
                        if active_status == expected_status:
                            print(f"Data found with matching status: {role_name} | {active_status}")
                            self.logger.info(
                                f"Status matched: {role_name} | {active_status}"
                            )
                            return True
                        else:
                            print(f"Status mismatch for {role_name}: expected {expected_status}, got {active_status}")
                            self.logger.error(
                                f"Status mismatch: {role_name} | Expected: {expected_status}, Got: {active_status}"
                            )
                            return False

                    return True

            self.logger.error(f"Product not found: {search_name}")
            return False

        except Exception as e:
            self.logger.error(f"Exception in search_product: {e}")
            return False

    def Click_refresh_btn(self):
        self.driver.find_element(*self.refresh_btn).click()

    def Enter_search_name_field(self,search_name):
        self.driver.find_element(*self.search_name_field).send_keys(search_name)

    def Click_filter_calender(self):
        self.driver.find_element(*self.filter_calender).click()

    def Choose_select_status(self, select_status):
        drpdwn = Select(self.driver.find_element(*self.select_status))
        drpdwn.select_by_visible_text(select_status)

    def Click_actions_icon(self):
        self.driver.find_element(*self.actions_icon).click()

    # def Click_inactive_opt(self):
    #     self.driver.find_element(*self.inactive_opt).click()

    def Click_active_opt(self):
        self.driver.find_element(*self.active_opt).click()

    def Click_Activate_btn(self):
        self.driver.find_element(*self.Activate_btn).click()

    def Click_Inactive_opt(self):
        self.driver.find_element(*self.Inactive_opt).click()

    def Click_suspend_btn(self):
        self.driver.find_element(*self.suspend_btn).click()


    # def Click_refresh_btn(self):
    #     self.wait.until(
    #         EC.element_to_be_clickable(self.refresh_btn)
    #     ).click()
    #
    # def Enter_search_name_field(self, search_name):
    #     search = self.wait.until(
    #         EC.visibility_of_element_located(self.search_name_field)
    #     )
    #     search.clear()
    #     search.send_keys(search_name)
    #
    # def Click_filter_calender(self):
    #     self.wait.until(
    #         EC.element_to_be_clickable(self.filter_calender)
    #     ).click()
    #
    # def Choose_select_status(self, select_status):
    #     dropdown = self.wait.until(
    #         EC.presence_of_element_located(self.select_status)
    #     )
    #     Select(dropdown).select_by_visible_text(select_status)
    #
    # def Click_actions_icon(self):
    #     self.wait.until(
    #         EC.element_to_be_clickable(self.actions_icon)
    #     ).click()
    #
    # def Click_active_opt(self):
    #     self.wait.until(
    #         EC.element_to_be_clickable(self.active_opt)
    #     ).click()
    #
    # def Click_Activate_btn(self):
    #     self.wait.until(
    #         EC.element_to_be_clickable(self.Activate_btn)
    #     ).click()
    #
    # def Click_Inactive_opt(self):
    #     self.wait.until(
    #         EC.element_to_be_clickable(self.Inactive_opt)
    #     ).click()
    #
    # def Click_suspend_btn(self):
    #     self.wait.until(
    #         EC.element_to_be_clickable(self.suspend_btn)
    #     ).click()
    #





