import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Generate_reports_download_page:
    Reports_tab=(By.XPATH,"//span[normalize-space()='Reports']")
    generate_reports = (By.XPATH, "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Generate Reports']")
    download_tab=(By.XPATH,"//a[normalize-space()='Downloads']")
    search_report_name=(By.XPATH,"//input[@id='search-vale']")
    created_at=(By.XPATH,"//input[@class='form-control dash-filter-picker active form-control input']")
    select_format=(By.XPATH,"//select[@id='format']")
    select_status=(By.XPATH,"//select[@id='idStatus']")
    refresh_btn=(By.XPATH,"//button[@class='btn btn-outline-primary btn-icon waves-effect waves-light reload_btn uicust-active-color uicust-active-border refresh_Btn ']")
    filters_toggle_btn=(By.XPATH,"//button[@id='filterToggleBtn']")
    filters_report_name=(By.XPATH,"//div[@class='mb-3']//input[@id='report_name']")
    filters_select_format=(By.XPATH,"//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Format']")
    filters_start_date=(By.XPATH,"//input[@id='start_date']")
    filters_end_date=(By.XPATH,"//input[@id='end_date']")
    filters_select_status=(By.XPATH,"//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Status']")
    created_date=(By.XPATH,"//input[@id='sb_date_range']")
    filters_apply_btn=(By.XPATH,"//button[normalize-space()='Apply']")
    filters_clr_btn=(By.XPATH,"//button[@id='clear-filter-btn']")
    create_Batch_status_report=(By.XPATH,"//select[@id='schedule_report_name']")
    create_select_format=(By.XPATH,"//select[@id='schedule_report_name']")
    create_choose_mail_receiving_duration=(By.XPATH,"//select[@id='mail_send_at']")
    create_select_duration=(By.XPATH,"//select[@id='duration']")



    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def Click_Reports_tab(self):
        self.driver.find_element(*self.Reports_tab).click()

    def Click_generate_reports(self):
        self.driver.find_element(*self.generate_reports).click()

    def Click_download_tab(self):
        self.driver.find_element(*self.download_tab).click()

    def Click_refresh_btn(self):
        self.driver.find_element(*self.refresh_btn).click()

    def Enter_search_report_name(self,report_name):
        self.driver.find_element(*self.search_report_name).send_keys(report_name)

    def Click_created_at(self):
        self.driver.find_element(*self.created_at).click()

    def Click_filters_toggle_btn(self):
        self.driver.find_element(*self.filters_toggle_btn).click()

    def Enter_filters_report_name(self,report_name):
        self.driver.find_element(*self.filters_report_name).send_keys(report_name)

    def Click_filters_start_date(self):
        self.driver.find_element(*self.filters_start_date).click()

    def Click_filters_end_date(self):
        self.driver.find_element(*self.filters_end_date).click()

    def Click_created_date(self):
        self.driver.find_element(*self.created_date).click()

    def Click_apply_btn(self):
        self.driver.find_element(*self.filters_apply_btn).click()

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

        # DAY - select only from the requested month
        days = self.driver.find_elements(
            By.XPATH,
            calendar_popup + "//span[contains(@class,'flatpickr-day')]"
        )

        date_selected = False

        for d in days:
            classes = d.get_attribute("class")

            if (
                    d.text == str(int(day))
                    and "prevMonthDay" not in classes
                    and "nextMonthDay" not in classes
                    and "disabled" not in classes
            ):
                d.click()
                date_selected = True
                break

        if not date_selected:
            raise Exception(
                f"Date {date_string} was not found in the selected calendar month."
            )

