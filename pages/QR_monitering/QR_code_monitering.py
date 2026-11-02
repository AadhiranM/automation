from datetime import time
import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class QR_code_monitering_page:

    # ================= DASHBOARD & QR =================
    Dashboard = (By.XPATH, "//span[@class='nav-name'][normalize-space()='Dashboard']")
    QR_Management = (By.XPATH, "//span[@class='nav-name'][normalize-space()='QR Management']")
    QR_monitering = (By.XPATH, "//span[contains(@class,'nav-name')][normalize-space()='QR Code Monitoring']")
    QR_code_monitering = (By.XPATH, "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='QR Code Monitoring']")

    # ================= SEARCH & FILTER =================
    search_field = (By.XPATH, "//input[@id='search-vale']")
    search_btn = (By.XPATH, "//button[@id='search-btn']")
    date_range_field = (By.XPATH, "//input[@id='datepicker-range']")
    select_status = (By.XPATH, "//select[@id='idStatus']")
    refresh_btn = (By.XPATH, "//button[contains(@class,'reload_btn') and contains(@class,'refresh_Btn')]")

    filter_toggle_btn = (By.XPATH, "//button[@id='filterToggleBtn']")
    scanned_at_field = (By.XPATH, "//input[@id='sidebar_scanned_at']")
    apply_btn = (By.XPATH, "//button[normalize-space()='Apply']")
    actions_icon = (By.XPATH, "//i[@class='ri-more-fill align-middle']")
    view_icon = (By.XPATH,"//ul[@class='dropdown-menu dropdown-menu-end dd_action show']//a[@class='dropdown-item'][normalize-space()='View']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ================= NAVIGATION =================
    def Click_Dashboard(self):
        self.wait.until(EC.element_to_be_clickable(self.Dashboard)).click()

    def Click_QR_management(self):
        self.wait.until(EC.element_to_be_clickable(self.QR_Management)).click()

    def Click_QR_monitering(self):
        self.wait.until(EC.element_to_be_clickable(self.QR_monitering)).click()

    def Click_QR_code_monitering(self):
        self.wait.until(EC.element_to_be_clickable(self.QR_code_monitering)).click()

    # ================= FILTER ACTIONS =================
    def Click_refresh_btn(self):
        self.wait.until(EC.element_to_be_clickable(self.refresh_btn)).click()

    def Enter_search_field(self, search_value):
        search = self.wait.until(EC.visibility_of_element_located(self.search_field))
        search.clear()
        search.send_keys(search_value)

    def Click_search_btn(self):
        self.wait.until(EC.element_to_be_clickable(self.search_btn)).click()

    def Enter_select_status(self, select_status):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.select_status))
        Select(dropdown).select_by_visible_text(select_status)

    def Click_date_range_field(self):
        self.wait.until(EC.element_to_be_clickable(self.date_range_field)).click()

    def Click_filter_toggle_btn(self):
        self.wait.until(EC.element_to_be_clickable(self.filter_toggle_btn)).click()

    def Click_scanned_at_field(self):
        self.wait.until(EC.element_to_be_clickable(self.scanned_at_field)).click()

    def Click_apply_btn(self):
        self.wait.until(EC.element_to_be_clickable(self.apply_btn)).click()

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
    def Click_actions_icon(self):
        actions_icon = self.wait.until(
            EC.visibility_of_element_located(self.actions_icon)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            actions_icon
        )

        self.wait.until(
            EC.element_to_be_clickable(self.actions_icon)
        ).click()

    def Click_view_icon(self):
        view_icon = self.wait.until(
            EC.visibility_of_element_located(self.view_icon)
        )

        self.wait.until(
            EC.element_to_be_clickable(self.view_icon)
        ).click()
