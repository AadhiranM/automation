import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Generate_reports_page:
    Reports_tab=(By.XPATH,"//span[normalize-space()='Reports']")
    schedule_report=(By.XPATH,"//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Schedule Reports']")
    search_field=(By.XPATH,"//input[@id='search-vale']")
    filter_By_date=(By.XPATH,"//input[@id='search-vale']")
    select_status=(By.XPATH,"//select[@id='idStatus']")
    create_btn=(By.XPATH,"//button[normalize-space()='Create']")
    search_btn=(By.XPATH,"//button[@id='search-btn']")
    refresh_btn=(By.XPATH,"//button[@class='btn btn-outline-primary btn-icon waves-effect waves-light reload_btn uicust-active-color uicust-active-border refresh_Btn ']")
    filters_toggle=(By.XPATH,"//button[@id='filterToggleBtn']")
    filters_report_name=(By.XPATH,"//input[@id='report_name']")
    filters_format=(By.XPATH,"//select[@id='format']")
    filters_nxt_schedule=(By.XPATH,"//input[@id='next_schedule_at']")
    filters_status=(By.XPATH,"//select[@id='status']")
    filters_apply_btn=(By.XPATH,"//button[normalize-space()='Apply']")
    create_btn_select_report=(By.XPATH,"//select[@id='schedule_report_name']")
    create_btn_select_format=(By.XPATH,"//select[@id='schedule_format']")
    create_btn_mail_receiving_duration=(By.XPATH,"//select[@id                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ='mail_send_at']")
    create_btn_select_duration=(By.XPATH,"//select[@id='duration']")
    Create_btn_save_btn=(By.XPATH,"//button[@id='submitReportBtn']")
    actions_icon=(By.XPATH,"//button[@class='btn btn-primary btn-sm dropdown']")
    deactivate=(By.XPATH,"//button[normalize-space()='Deactivate']")
    activate=(By.XPATH,"//button[normalize-space()='Activate']")
    yes_deactivate_button=(By.XPATH,"//button[normalize-space()='Yes, deactivate']")
    yes_activate_button=(By.XPATH,"//button[normalize-space()='Yes, activate']")
    submitted_ok_btn=(By.XPATH,"//button[normalize-space()='OK']")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ================= NAVIGATION =================
    def Click_reports_tab(self):
        self.driver.find_element(*self.Reports_tab).click()

    def Click_schedule_report(self):
        self.driver.find_element(*self.schedule_report).click()

    def Click_create_btn(self):
        self.driver.find_element(*self.create_btn).click()

    def choose_create_btn_select_report(self,select_report):
        drpdwn = Select(self.driver.find_element(*self.create_btn_select_report))
        drpdwn.select_by_visible_text(select_report)

    def choose_create_btn_select_format(self,select_format):
        drpdwn = Select(self.driver.find_element(*self.create_btn_select_format))
        drpdwn.select_by_visible_text(select_format)

    def choose_create_btn_mail_receiving_duration(self,mail_receiving_duration):
        drpdwn = Select(self.driver.find_element(*self.create_btn_mail_receiving_duration))
        drpdwn.select_by_visible_text(mail_receiving_duration)

    def choose_create_btn_select_duration(self,select_duration):
        drpdwn = Select(self.driver.find_element(*self.create_btn_select_duration))
        drpdwn.select_by_visible_text(select_duration)

    def Click_Create_btn_save_btn(self):
        self.driver.find_element(*self.Create_btn_save_btn).click()

    def Click_filters_toggle(self):
        self.driver.find_element(*self.filters_toggle).click()

    def Click_filters_report_name(self,report_name):
        self.driver.find_element(*self.filters_report_name).send_keys(report_name)

    def Choose_filters_format(self,select_format):
        drpdwn = Select(self.driver.find_element(*self.filters_format))
        drpdwn.select_by_visible_text(select_format)

    def Choose_filters_status(self,select_status):
        drpdwn = Select(self.driver.find_element(*self.filters_status))
        drpdwn.select_by_visible_text(select_status)

    def Click_filters_nxt_schedule(self):
        self.driver.find_element(*self.filters_nxt_schedule).click()

    def select_date(self, date_string):
        day, month, year = date_string.split("-")
        month_name = calendar.month_name[int(month)]

        calendar_popup = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]"

        # YEAR
        year_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, calendar_popup + "//input[@aria-label='Year']")
            )
        )
        year_input.click()
        year_input.clear()
        year_input.send_keys(year)

        # MONTH
        month_dropdown = Select(
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, calendar_popup + "//select[@aria-label='Month']")
                )
            )
        )
        month_dropdown.select_by_visible_text(month_name)

            # DAY
        days = self.driver.find_elements(
            By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"
        )
        for d in days:
            if d.text == day and "disabled" not in d.get_attribute("class"):
                d.click()
                break
        time.sleep(2)

    def set_filters_nxt_schedule(self, date_string):
        self.wait.until(EC.element_to_be_clickable(self.filters_nxt_schedule)).click()
        self.select_date(date_string)

    def Click_filters_apply_btn(self):
        self.driver.find_element(*self.filters_apply_btn).click()

    def search_product(self, report_name):
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
                product_name = self.driver.find_element(
                    By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[2]"
                ).text.strip()
                # batch_no = self.driver.find_element(
                #     By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[3]"
                # ).text.strip()
                time.sleep(1)

                print(product_name)
                if report_name == product_name:

                    flag = True
                    break

        except Exception as e:
            print(f"Exception in searching product: {e}")
            flag = False

        return flag

    def Click_actions_button(self):
        self.driver.find_element(*self.actions_icon).click()

    def Click_deactivate_icon(self):
        self.driver.find_element(*self.deactivate).click()

    def Click_activate_icon(self):
        self.driver.find_element(*self.activate).click()

    def Click_yes_deactivate_btn(self):
        self.driver.find_element(*self.yes_deactivate_button).click()

    def Click_yes_activate_btn(self):
        self.driver.find_element(*self.yes_activate_button).click()

    def Click_submitted_ok_btn(self):
        self.driver.find_element(*self.submitted_ok_btn).click()









