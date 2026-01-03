# from calendar import calendar
# from datetime import time
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# class QR_Management_Category_Page:
#    ## Xpath for all the elements
#     Dashboard=(By.XPATH,"//span[@class='nav-name'][normalize-space()='Dashboard']")
#     QR_Management= (By.XPATH, "//span[@class='nav-name'][normalize-space()='QR Management']")
#     QR_monitering= (By.XPATH, "//span[contains(@class,'nav-name')][normalize-space()='QR Code Monitoring']")
#     QR_code_monitering=(By.XPATH,"//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='QR Code Monitoring']")
#     search_field=(By.XPATH,"//input[@id='search-vale']")
#     date_range_field=(By.XPATH,"//input[@id='datepicker-range']")
#     select_status=(By.XPATH,"//select[@id='idStatus']")
#     refresh_btn=(By.XPATH,"//button[@class='btn btn-outline-primary btn-icon waves-effect waves-light reload_btn uicust-active-color uicust-active-border refresh_Btn ']")
#     export_btn=(By.XPATH,"//button[normalize-space()='Export']")
#     filters_btn=(By.XPATH,"//button[@id='filterToggleBtn']")
#     filters_username=(By.XPATH,"//input[@id='user_name']")
#     filters_usermobile=(By.XPATH,"//input[@id='user_mobile']")
#     filters_deviceName=(By.XPATH,"//input[@id='device_name']")
#     scanned_date=(By.XPATH,"//input[@id='scanned_at']")
#     filters_apply=(By.XPATH,"//button[normalize-space()='Apply']")
#     report_start_id=(By.XPATH,"//input[@id='fromId']")
#     report_end_id=(By.XPATH,"//input[@id='toId']")
#     ID_select_user_drpdwn=(By.XPATH,"//select[@id='id-user-select']")
#     submit_btn=(By.XPATH,"//button[@id='submitBtn']")
#     user_based_btn=(By.XPATH,"//button[@id='user-tab']")
#     select_user_opt=(By.XPATH,"//div[@data-type='select-one']//div[@class='choices__inner']")
#     User_select_user_drpdwn=(By.XPATH,"//select[@id='export-user-select']")
#     User_date_range=(By.XPATH,"//input[@id='export_datepicker_range']")
#     bulk_id_tab=(By.XPATH,"//button[@id='bulk-tab']")
#     enter_bulk_id=(By.XPATH,"//textarea[@id='bulkId']")
#     date_based_tab=(By.XPATH,"//button[@id='date-tab']")
#     date_based_date_range=(By.XPATH,"//button[@id='date-tab']")
#
#     def __init__(self, driver):
#         self.driver = driver
#         self.wait = WebDriverWait(driver, 10)
#
#     # Actions
#     def Click_Dashboard(self):
#         self.driver.find_element(*self.Dashboard).click()
#
#     def Click_QR_monitering(self):
#         self.driver.find_element(*self.QR_monitering).click()
#
#     def Click_QR_code_monitering(self):
#         self.driver.find_element(*self.QR_code_monitering).click()
#
#     def Click_refresh_btn(self):
#         self.driver.find_element(*self.refresh_btn).click()
#
#     def Click_filters_btn(self):
#         self.driver.find_element(*self.filters_btn).click()
#
#     def Enter_filters_username(self,username):
#         self.driver.find_element(*self.filters_username).clear()
#         self.driver.find_element(*self.filters_username).send_keys(username)
#
#     def Enter_filters_usermobile(self,usermobile):
#         self.driver.find_element(*self.filters_usermobile).clear()
#         self.driver.find_element(*self.filters_usermobile).send_keys(usermobile)
#
#     def Enter_device_name(self,deviceName):
#         self.driver.find_element(*self.filters_deviceName).clear()
#         self.driver.find_element(*self.filters_deviceName).send_keys(deviceName)
#
#     def Click_scanned_date(self):
#         self.driver.find_element(*self.scanned_date).click()
#
#
#
# def select_date_range(self, start_date, end_date):
#     """
#     Selects a date range on Flatpickr (range mode)
#
#     :param start_date: YYYY-MM-DD
#     :param end_date: YYYY-MM-DD
#     """
#
#     start_year, start_month, start_day = start_date.split("-")
#     end_year, end_month, end_day = end_date.split("-")
#
#     start_month_name = calendar.month_name[int(start_month)]
#     end_month_name = calendar.month_name[int(end_month)]
#
#     calendar_popup = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]"
#
#     # Wait for calendar to be visible
#     self.wait.until(
#         EC.visibility_of_element_located((By.XPATH, calendar_popup))
#     )
#
#     # -------------------------
#     # SET START YEAR & MONTH
#     # -------------------------
#     year_input = self.wait.until(
#         EC.element_to_be_clickable(
#             (By.XPATH, calendar_popup + "//input[@aria-label='Year']")
#         )
#     )
#     year_input.clear()
#     year_input.send_keys(start_year)
#
#     month_dropdown = Select(
#         self.wait.until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, calendar_popup + "//select[@aria-label='Month']")
#             )
#         )
#     )
#     month_dropdown.select_by_visible_text(start_month_name)
#
#     time.sleep(0.5)
#
#     # -------------------------
#     # SELECT START DAY
#     # -------------------------
#     start_days = self.driver.find_elements(
#         By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"
#     )
#
#     for day in start_days:
#         if day.text == str(int(start_day)) and "disabled" not in day.get_attribute("class"):
#             day.click()
#             break
#
#     time.sleep(0.5)
#
#     # -------------------------
#     # SET END YEAR & MONTH (if needed)
#     # -------------------------
#     if start_year != end_year or start_month_name != end_month_name:
#
#         year_input = self.wait.until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, calendar_popup + "//input[@aria-label='Year']")
#             )
#         )
#         year_input.clear()
#         year_input.send_keys(end_year)
#
#         month_dropdown = Select(
#             self.wait.until(
#                 EC.element_to_be_clickable(
#                     (By.XPATH, calendar_popup + "//select[@aria-label='Month']")
#                 )
#             )
#         )
#         month_dropdown.select_by_visible_text(end_month_name)
#
#         time.sleep(0.5)
#
#     # -------------------------
#     # SELECT END DAY
#     # -------------------------
#     end_days = self.driver.find_elements(
#         By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"
#     )
#
#     for day in end_days:
#         if day.text == str(int(end_day)) and "disabled" not in day.get_attribute("class"):
#             day.click()
#             break
#
#     time.sleep(1)

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
    QR_code_monitering = (
        By.XPATH,
        "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='QR Code Monitoring']"
    )

    # ================= SEARCH & FILTER =================
    search_field = (By.XPATH, "//input[@id='search-vale']")
    date_range_field = (By.XPATH, "//input[@id='datepicker-range']")
    select_status = (By.XPATH, "//select[@id='idStatus']")
    refresh_btn = (
        By.XPATH,
        "//button[contains(@class,'reload_btn') and contains(@class,'refresh_Btn')]"
    )
    export_btn = (By.XPATH, "//button[normalize-space()='Export']")
    filters_btn = (By.XPATH, "//button[@id='filterToggleBtn']")

    # ================= FILTER POPUP =================
    filters_username = (By.XPATH, "//input[@id='user_name']")
    filters_usermobile = (By.XPATH, "//input[@id='user_mobile']")
    filters_deviceName = (By.XPATH, "//input[@id='device_name']")
    scanned_date = (By.XPATH, "//input[@id='scanned_at']")
    filters_apply = (By.XPATH, "//button[normalize-space()='Apply']")

    # ================= REPORT EXPORT =================
    report_start_id = (By.XPATH, "//input[@id='fromId']")
    report_end_id = (By.XPATH, "//input[@id='toId']")
    ID_select_user_drpdwn = (By.XPATH,"//select[@id='id-user-select']")
    submit_btn = (By.XPATH, "//button[@id='submitBtn']")

    # ================= USER EXPORT =================
    user_based_btn = (By.XPATH, "//button[@id='user-tab']")
    select_user_opt = (By.XPATH, "//div[@data-type='select-one']//div[@class='choices__inner']")
    User_select_user_drpdwn = (By.XPATH, "//select[@id='export-user-select']")
    User_date_range = (By.XPATH, "//input[@id='export_datepicker_range']")

    # ================= BULK EXPORT =================
    bulk_id_tab = (By.XPATH, "//button[@id='bulk-tab']")
    enter_bulk_id = (By.XPATH, "//textarea[@id='bulkId']")

    # ================= DATE BASED EXPORT =================
    date_based_tab = (By.XPATH, "//button[@id='date-tab']")
    date_based_date_range = (By.XPATH, "//input[@id='export_datepicker_range']")
    table_rows = (By.XPATH, "//table[@id='crudTable']//tbody//tr")

    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ================= NAVIGATION =================
    def Click_Dashboard(self):
        self.driver.find_element(*self.Dashboard).click()

    def Click_QR_management(self):
        self.driver.find_element(*self.QR_Management).click()

    def Click_QR_monitering(self):
        self.driver.find_element(*self.QR_monitering).click()

    def Click_QR_code_monitering(self):
        self.driver.find_element(*self.QR_code_monitering).click()

    # ================= FILTER ACTIONS =================
    def Click_refresh_btn(self):
        self.driver.find_element(*self.refresh_btn).click()

    def Click_filters_btn(self):
        self.driver.find_element(*self.filters_btn).click()

    def Enter_filters_username(self, username):
        field = self.driver.find_element(*self.filters_username)
        field.clear()
        field.send_keys(username)

    def Enter_filters_usermobile(self, usermobile):
        field = self.driver.find_element(*self.filters_usermobile)
        field.clear()
        field.send_keys(usermobile)

    def Enter_device_name(self, device_name):
        field = self.driver.find_element(*self.filters_deviceName)
        field.clear()
        field.send_keys(device_name)

    def Click_scanned_date(self):
        self.driver.find_element(*self.scanned_date).click()

    def Click_filters_apply(self):
        self.driver.find_element(*self.filters_apply).click()

    def click_Export_btn(self):
        self.driver.find_element(*self.export_btn).click()

    def Enter_report_start_id(self,Report_start_Id):
        self.driver.find_element(*self.report_start_id).send_keys(Report_start_Id)

    def Enter_report_end_id(self,Report_end_Id):
        self.driver.find_element(*self.report_end_id).send_keys(Report_end_Id)

    def select_id_select_user_drpdwn(self,select_user):
        drpdwn= Select(self.driver.find_element(*self.ID_select_user_drpdwn))
        drpdwn.select_by_visible_text(select_user)

    def click_submit_btn(self):
        self.driver.find_element(*self.submit_btn).click()


    # ================= FLATPICKR DATE RANGE =================
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

    def search_product(self, timeout=10):
        """
        Check if the QR Monitoring table has any rows after applying filter.
        Returns True if table has rows, False if empty.
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            wait = WebDriverWait(self.driver, timeout)
            # Wait until table is present
            wait.until(EC.presence_of_element_located((By.ID, "crudTable")))

            # Check if table shows "No data"
            empty_cells = self.driver.find_elements(
                By.XPATH, "//table[@id='crudTable']//td[@class='dataTables_empty']"
            )
            if empty_cells:
                print("Table is empty")
                return False

            # Check for rows
            rows = self.driver.find_elements(By.XPATH, "//table[@id='crudTable']//tbody//tr")
            if not rows:
                print("No rows found")
                return False

            print(f"Table has {len(rows)} row(s)")
            for r, row in enumerate(rows, start=1):
                tds = row.find_elements(By.TAG_NAME, "td")
                row_data = [td.text.strip() for td in tds]
                print(f"Row {r}: {row_data}")

            return True

        except Exception as e:
            print(f"Exception in checking table rows: {e}")
            return False

    def get_table_row_count(self):
        """
        Returns the number of rows in the table after filter is applied.
        Correctly handles 'No data available' row.
        """
        rows = self.driver.find_elements(*self.table_rows)
        if not rows:
            return 0
        # Check if first row shows "No data"
        if "dataTables_empty" in rows[0].get_attribute("class"):
            return 0
        return len(rows)
