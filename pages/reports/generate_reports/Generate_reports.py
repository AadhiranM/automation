# import time
# import calendar
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# class Generate_reports_page:
#     Reports_tab=(By.XPATH,"//span[normalize-space()='Reports']")
#     generate_reports=(By.XPATH,"//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Generate Reports']")
#     Batch_status_report=(By.XPATH,"//a[@data-title='Batch Status Report']")
#     scan_analytics_report=(By.XPATH,"//a[@data-title='Scan Analytics Report']")
#     product_analytics_report=(By.XPATH,"//a[@data-title='Product Analysis Report']")
#     fraud_detection_report=(By.XPATH,"//a[@data-title='Fraud Detection Report']")
#     print_Audit_report=(By.XPATH,"//a[@data-title='Print Audit Report']")
#
#     report_name=(By.XPATH,"//div[@class='row g-3']//div[@class='col-lg-12']//input[@id='report_name']")
#     select_format=(By.XPATH,"//select[@id='selectFormat']")
#     select_duration=(By.XPATH,"//select[@id='selectDuration']")
#     generate_btn=(By.XPATH,"//button[@id='add_report']")
#
#     def __init__(self, driver):
#         self.driver = driver
#         self.wait = WebDriverWait(driver, 15)
#
#     # ================= NAVIGATION =================
#     def Click_reports_tab(self):
#         self.driver.find_element(*self.Reports_tab).click()
#
#     def Click_generate_report(self):
#         self.driver.find_element(*self.generate_reports).click()
#
#     def Click_Batch_status_reports(self):
#         self.driver.find_element(*self.Batch_status_report).click()
#
#     def Click_scan_analytics_reports(self):
#         self.driver.find_element(*self.scan_analytics_report).click()
#
#     def Click_product_analytics_report(self):
#         self.driver.find_element(*self.product_analytics_report).click()
#
#     def Click_fraud_detection_report(self):
#         self.driver.find_element(*self.fraud_detection_report).click()
#
#     def Click_print_Audit_report(self):
#         self.driver.find_element(*self.print_Audit_report).click()
#
#     def Enter_report_name(self,report_name):
#         self.driver.find_element(*self.report_name).send_keys(report_name)
#
#     def choose_select_format(self,select_format):
#         drpdwn = Select(self.driver.find_element(*self.select_format))
#         drpdwn.select_by_visible_text(select_format)
#
#     def choose_select_duration(self,select_duration):
#         drpdwn = Select(self.driver.find_element(*self.select_duration))
#         drpdwn.select_by_visible_text(select_duration)
#
#     def Click_generate_btn(self):
#         self.driver.find_element(*self.generate_btn).click()




import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Generate_reports_page:
    Reports_tab = (By.XPATH, "//span[normalize-space()='Reports']")
    generate_reports = (By.XPATH, "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Generate Reports']")
    Batch_status_report = (By.XPATH, "//a[@data-title='Batch Status Report']")
    scan_analytics_report = (By.XPATH, "//a[@data-title='Scan Analytics Report']")
    product_analytics_report = (By.XPATH, "//a[@data-title='Product Analysis Report']")
    fraud_detection_report = (By.XPATH, "//a[@data-title='Fraud Detection Report']")
    print_Audit_report = (By.XPATH, "//a[@data-title='Print Audit Report']")

    report_name = (By.XPATH, "//div[@class='row g-3']//div[@class='col-lg-12']//input[@id='report_name']")
    select_format = (By.XPATH, "//select[@id='selectFormat']")
    select_duration = (By.XPATH, "//select[@id='selectDuration']")
    generate_btn = (By.XPATH, "//button[@id='add_report']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ================= NAVIGATION =================
    def Click_reports_tab(self):
        self.wait.until(
            EC.element_to_be_clickable(self.Reports_tab)
        ).click()

    def Click_generate_report(self):
        self.wait.until(
            EC.element_to_be_clickable(self.generate_reports)
        ).click()

    def Click_Batch_status_reports(self):
        self.wait.until(
            EC.element_to_be_clickable(self.Batch_status_report)
        ).click()

    def Click_scan_analytics_reports(self):
        self.wait.until(
            EC.element_to_be_clickable(self.scan_analytics_report)
        ).click()

    def Click_product_analytics_report(self):
        self.wait.until(
            EC.element_to_be_clickable(self.product_analytics_report)
        ).click()

    def Click_fraud_detection_report(self):
        self.wait.until(
            EC.element_to_be_clickable(self.fraud_detection_report)
        ).click()

    def Click_print_Audit_report(self):
        self.wait.until(
            EC.element_to_be_clickable(self.print_Audit_report)
        ).click()

    def Enter_report_name(self, report_name):
        field = self.wait.until(
            EC.visibility_of_element_located(self.report_name)
        )
        field.clear()
        field.send_keys(report_name)

    def choose_select_format(self, select_format):
        dropdown = self.wait.until(
            EC.element_to_be_clickable(self.select_format)
        )
        Select(dropdown).select_by_visible_text(select_format)

    def choose_select_duration(self, select_duration):
        dropdown = self.wait.until(
            EC.element_to_be_clickable(self.select_duration)
        )
        Select(dropdown).select_by_visible_text(select_duration)

    def Click_generate_btn(self):
        self.wait.until(
            EC.element_to_be_clickable(self.generate_btn)
        ).click()

    def click_report_download_btn(self, report_name):
        try:
            report_name_text = self.driver.find_element(
                By.XPATH, "//table[@id='crudTable']//tbody//tr[1]//td[2]"
            ).text.strip()

            time.sleep(1)
            print("Report name:", report_name_text)

            if report_name_text == report_name:

                status = self.driver.find_element(
                    By.XPATH, "//table[@id='crudTable']//tbody//tr[1]//td[7]"
                ).text.strip()

                print("Status of the report:", status)

                action_btn = self.driver.find_elements(
                    By.XPATH, "//table[@id='crudTable']//tbody//tr[1]//td[9]//a"
                )

                if action_btn:
                    print("Download option is present")

                else:
                    print("Download option is not present")

                    no_data = self.driver.find_element(
                        By.XPATH, "//table[@id='crudTable']//tbody//tr[1]//td[9]"
                    )

                    print("No data available:", no_data.text.strip())

            else:
                print("Report name does not match")

        except Exception as e:
            print("Error while checking report download option:", e)
