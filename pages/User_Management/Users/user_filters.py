import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.customlogger import LogGen

class user_filters:
    Dashboard = (By.XPATH, "//span[@class='nav-name'][normalize-space()='Dashboard']")
    user_management_opt=(By.XPATH,"//span[normalize-space()='User Management']")
    users=(By.XPATH,"//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Users']")
    refresh_btn=(By.XPATH,"//button[contains(@class,'btn btn-outline-primary btn-icon waves-effect waves-light reload_btn uicust-active-color uicust-active-border refresh_Btn')]")
    filters_btn=(By.XPATH,"//button[@id='filterToggleBtn']")
    search_field=(By.XPATH,"//input[@id='search-vale']")
    filter_calender=(By.XPATH,"//input[@class='form-control dash-filter-picker active form-control input']")
    select_status=(By.XPATH,"//select[@id='idStatus']")
    actions_icon=(By.XPATH,"(//button[@type='button'])[14]")
    suspend_opt=(By.XPATH,"//a[normalize-space()='Suspend']")
    yes_btn=(By.XPATH,"//button[normalize-space()='Yes']")
    Activate_opt=(By.XPATH,"//a[normalize-space()='Activate']")
    Activate_btn=(By.XPATH,"//button[normalize-space()='Activate']")

    #filter_toggle
    filter_toggle=(By.XPATH,"//button[@id='filterToggleBtn']")
    filter_toggle_name_field=(By.XPATH,"//input[@id='name']")
    filter_toggle_created_by_opt=(By.XPATH,"//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Created By']")
    filter_toggle_created_By_field=(By.XPATH,"//input[@placeholder='Search Created By']")
    filter_toggle_role_opt=(By.XPATH,"//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Role']")
    filter_toggle_role_field=(By.XPATH,"//input[@aria-label='Select Role']")
    filter_toggle_user_type_opt=(By.XPATH,"//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select User Type']")
    filter_toggle_user_type_field=(By.XPATH,"//input[@aria-label='Select User Type']")
    filter_toggle_apply_btn=(By.XPATH,"//button[normalize-space()='Apply']")



    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = LogGen.loggen()

    # ================= NAVIGATION =================
    def Click_Dashboard(self):
        self.driver.find_element(*self.Dashboard).click()

    def Click_User_management(self):
        self.driver.find_element(*self.user_management_opt).click()

    def Click_users(self):
        self.driver.find_element(*self.users).click()

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


        time.sleep(1)

        # END DATE
        if start_year != end_year or start_month_name != end_month_name:
            year_input.clear()
            year_input.send_keys(end_year)
            month_dropdown.select_by_visible_text(end_month_name)
            time.sleep(1)

        for d in self.driver.find_elements(By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"):
            classes = d.get_attribute("class")
            if (
                    d.text == str(int(end_day))
                    and "flatpickr-disabled" not in classes
                    and "notAllowed" not in classes
                    and "prevMonthDay" not in classes
                    and "nextMonthDay" not in classes
            ):
                d.click()
                break

        time.sleep(1)



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
                    By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[8]"
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

    def Enter_search_field(self,search_name):
        self.driver.find_element(*self.search_field).send_keys(search_name)

    def Click_filter_calender(self):
        self.driver.find_element(*self.filter_calender).click()

    def Choose_select_status(self, select_status):
        drpdwn = Select(self.driver.find_element(*self.select_status))
        drpdwn.select_by_visible_text(select_status)

    def Click_actions_icon(self):
        self.driver.find_element(*self.actions_icon).click()

    def Click_yes_btn(self):
        self.driver.find_element(*self.yes_btn).click()

    def Click_activate_opt(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.Activate_opt)
        ).click()

    def Click_suspend_opt(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.suspend_opt)
        ).click()

    def Click_Activate_btn(self):
        self.driver.find_element(*self.Activate_btn).click()

    ###filter_toggle

    def Click_filter_toggle(self):
        self.driver.find_element(*self.filter_toggle).click()

    def Enter_filter_toggle_name(self, name):
        self.driver.find_element(*self.filter_toggle_name_field).send_keys(name)

    def Click_filter_toggle_created_by_opt(self):
        self.driver.find_element(*self.filter_toggle_created_by_opt).click()

    def Enter_filter_toggle_created_by_field(self, created_by):
        element=self.driver.find_element(*self.filter_toggle_created_By_field)
        element.send_keys(created_by)
        element.send_keys(Keys.ENTER)
        # self.driver.find_element(*self.filter_toggle_created_By_field).send_keys(created_by)

    def Click_filter_toggle_role_opt(self):
        self.driver.find_element(*self.filter_toggle_role_opt).click()

    def Enter_filter_toggle_role_field(self, role):

        self.driver.find_element(*self.filter_toggle_role_field).send_keys(role)

    def Click_filter_toggle_user_type_opt(self):
        self.driver.find_element(*self.filter_toggle_user_type_opt).click()

    def Enter_filter_toggle_user_type_field(self, user_type):
        element=self.driver.find_element(*self.filter_toggle_user_type_field)
        element.send_keys(user_type)
        element.send_keys(Keys.ENTER)
        # self.driver.find_element(*self.filter_toggle_user_type_field).send_keys(user_type)

    def Click_filter_toggle_apply_btn(self):
        self.driver.find_element(*self.filter_toggle_apply_btn).click()





