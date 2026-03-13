import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class user_filters:
    Dashboard = (By.XPATH, "//span[@class='nav-name'][normalize-space()='Dashboard']")
    user_management_opt=(By.XPATH,"//span[normalize-space()='User Management']")
    users=(By.XPATH,"//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Users']")
    refresh_btn=(By.XPATH,"//button[contains(@class,'btn btn-outline-primary btn-icon waves-effect waves-light reload_btn uicust-active-color uicust-active-border refresh_Btn')]")
    filters_btn=(By.XPATH,"//button[@id='filterToggleBtn']")
    search_field=(By.XPATH,"//input[@id='search-vale']")
    filter_calender=(By.XPATH,"//input[@id='datepicker-range']")
    select_status=(By.XPATH,"//select[@id='idStatus']")
    actions_icon=(By.XPATH,"(//button[@type='button'])[12]")
    suspend=(By.XPATH,"//ul[@class='dropdown-menu dropdown-menu-end show']//a[@class='dropdown-item status-item-btn'][normalize-space()='Suspend']")
    yes_Iam_sure_btn=(By.XPATH,"//button[@class='btn btn-danger status-record']")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

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

        # for d in self.driver.find_elements(By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"):
        #     if d.text == str(int(start_day)) and "disabled" not in d.get_attribute("class"):
        #         d.click()
        #         break

        time.sleep(2)

        # END DATE
        if start_year != end_year or start_month_name != end_month_name:
            year_input.clear()
            year_input.send_keys(end_year)
            month_dropdown.select_by_visible_text(end_month_name)
            time.sleep(2)

        for d in self.driver.find_elements(By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"):
            if d.text == str(int(end_day)) and "disabled" not in d.get_attribute("class"):
                d.click()
                break

        time.sleep(1)

    def search_product(self, search_name):
        flag = False
        try:
            # Check if table has empty message
            empty_cells = self.driver.find_elements(By.XPATH, "//table[@id='crudTable']//td[@class='dataTables_empty']")
            if empty_cells:
                print("Table is empty")
                return False

            # Get all rows in tbody
            rows = self.driver.find_elements(By.XPATH, "//table[@id='crudTable']//tbody//tr")

            for r in range(1, len(rows) + 1):
                # Get product_name and batch_no using full XPath
                search_result = self.driver.find_element(
                    By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[2]"
                ).text.strip()
                # batch_no = self.driver.find_element(
                #     By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[3]"
                # ).text.strip()
                time.sleep(1)

                print(search_result)
                if search_name == search_result:

                    flag = True
                    break

        except Exception as e:
            print(f"Exception in searching product: {e}")
            flag = False

        return flag


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

    def Click_suspend_opt(self):
        self.driver.find_element(*self.suspend).click()

    def Click_yes_Iam_sure_btn(self):
        self.driver.find_element(*self.yes_Iam_sure_btn).click()






