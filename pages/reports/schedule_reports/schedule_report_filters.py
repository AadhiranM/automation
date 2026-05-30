import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.customlogger import LogGen
class Generate_reports_page:
    Reports_tab=(By.XPATH,"//span[normalize-space()='Reports']")
    schedule_report=(By.XPATH,"//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Schedule Reports']")
    search_field=(By.XPATH,"//input[@id='search-vale']")
    filter_By_date=(By.XPATH,"//input[@id='datepicker-range']")
    select_status=(By.XPATH,"//select[@id='idStatus']")
    create_btn=(By.XPATH,"//button[normalize-space()='Create']")
    search_btn=(By.XPATH,"//button[@id='search-btn']")
    refresh_btn=(By.XPATH,"//button[@class='btn btn-outline-primary btn-icon waves-effect waves-light reload_btn uicust-active-color uicust-active-border refresh_Btn ']")
    filters_toggle=(By.XPATH,"//button[@id='filterToggleBtn']")
    filters_report_name=(By.XPATH,"//input[@id='report_name']")
    filters_format=(By.XPATH,"//select[@id='format']")
    filters_nxt_schedule=(By.XPATH,"//input[@id='next_schedule_at']")
    filter_status=(By.XPATH,"//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Status']")
    filters_status=(By.XPATH,"//select[@id='sb_status']")
    filters_apply_btn=(By.XPATH,"//button[normalize-space()='Apply']")
    create_btn_select_report=(By.XPATH,"//select[@id='schedule_report_name']")
    create_btn_select_format=(By.XPATH,"//select[@id='schedule_format']")
    create_btn_mail_receiving_duration=(By.XPATH,"//select[@id                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ='mail_send_at']")
    create_btn_select_duration=(By.XPATH,"//select[@id='duration']")
    Create_btn_save_btn=(By.XPATH,"//button[@id='submitReportBtn']")
    actions_icon=(By.XPATH,"//button[@class='btn btn-primary btn-sm dropdown']")
    deactivate=(By.XPATH,"//button[normalize-space()='Deactivate']")
    activate=(By.XPATH,"//button[normalize-space()='Activate']")
    deactivate_button=(By.XPATH,"//button[normalize-space()='deactivate']")
    activate_button=(By.XPATH,"//button[normalize-space()='activate']")
    submitted_ok_btn=(By.XPATH,"//button[normalize-space()='OK']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.logger = LogGen.loggen()

    # ================= NAVIGATION =================
    def Click_reports_tab(self):
        self.driver.find_element(*self.Reports_tab).click()

    def Click_schedule_report(self):
        self.driver.find_element(*self.schedule_report).click()

    def Click_create_btn(self):
        self.driver.find_element(*self.create_btn).click()

    def choose_create_btn_select_report(self,select_report):
        drpdwn=Select(self.driver.find_element(*self.create_btn_select_report))
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
        # self.driver.find_element(*self.filter_status).click()
        drpdwn = Select(self.driver.find_element(*self.filters_status))
        drpdwn.select_by_visible_text(select_status)

    def Click_filters_nxt_schedule(self):
        self.driver.find_element(*self.filters_nxt_schedule).click()

    def Click_search_field(self,search_value):
        search_input = self.driver.find_element(*self.search_field)
        search_input.clear()
        search_input.send_keys(search_value)
        search_input.send_keys(Keys.ENTER)

    def Click_filter_By_date(self):
        self.driver.find_element(*self.filter_By_date).click()

    def choose_select_status(self,select_status):
        drpdwn = Select(self.driver.find_element(*self.select_status))
        drpdwn.select_by_visible_text(select_status)


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
                    By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[11]"
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

    def Click_actions_button(self):
        self.driver.find_element(*self.actions_icon).click()

    def Click_deactivate_icon(self):
        self.driver.find_element(*self.deactivate).click()

    def Click_activate_icon(self):
        self.driver.find_element(*self.activate).click()

    def Click_deactivate_btn(self):
        self.driver.find_element(*self.deactivate_button).click()

    def Click_activate_btn(self):
        self.driver.find_element(*self.activate_button).click()

    def Click_submitted_ok_btn(self):
        self.driver.find_element(*self.submitted_ok_btn).click()









