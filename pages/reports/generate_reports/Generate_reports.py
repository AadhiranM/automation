import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Generate_reports_page:
    Reports_tab=(By.XPATH,"//span[normalize-space()='Reports']")
    generate_reports=(By.XPATH,"//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Generate Reports']")
    Batch_status_report=(By.XPATH,"//a[@data-title='Batch Status Report']//i[@class='ri-file-chart-line']")
    scan_analytics_report=(By.XPATH,"//a[@data-title='Scan Analytics Report']//i[@class='ri-file-chart-line']")
    product_analytics_report=(By.XPATH,"//a[@data-title='Product Analysis Report']//i[@class='ri-file-chart-line']")
    fraud_detection_report=(By.XPATH,"//a[@data-title='Fraud Detection Report']//i[@class='ri-file-chart-line']")
    print_Audit_report=(By.XPATH,"//a[@data-title='Print Audit Report']//i[@class='ri-file-chart-line']")

    report_name=(By.XPATH,"//div[@class='row g-3']//div[@class='col-lg-12']//input[@id='report_name']")
    select_format=(By.XPATH,"//label[contains(normalize-space(.),'Select Format')]/parent::div//select")
    select_duration=(By.XPATH,"//select[@class='form-select list_date report_duration']")
    generate_btn=(By.XPATH,"//button[@id='add_report']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ================= NAVIGATION =================
    def Click_reports_tab(self):
        self.driver.find_element(*self.Reports_tab).click()

    def Click_generate_report(self):
        self.driver.find_element(*self.generate_reports).click()

    def Click_Batch_status_reports(self):
        self.driver.find_element(*self.Batch_status_report).click()

    def Click_scan_analytics_reports(self):
        self.driver.find_element(*self.scan_analytics_report).click()

    def Click_product_analytics_report(self):
        self.driver.find_element(*self.product_analytics_report).click()

    def Click_fraud_detection_report(self):
        self.driver.find_element(*self.fraud_detection_report).click()

    def Click_print_Audit_report(self):
        self.driver.find_element(*self.print_Audit_report).click()

    def Enter_report_name(self,report_name):
        self.driver.find_element(*self.report_name).send_keys(report_name)

    def choose_select_format(self,select_format):
        drpdwn = Select(self.driver.find_element(*self.select_format))
        drpdwn.select_by_visible_text(select_format)

    def choose_select_duration(self,select_duration):
        drpdwn = Select(self.driver.find_element(*self.select_duration))
        drpdwn.select_by_visible_text(select_duration)

    def Click_generate_btn(self):
        self.driver.find_element(*self.generate_btn).click()

    def click_report_download_btn(self, report_name):
        try:
            report_name_text = self.driver.find_element(
                By.XPATH, "//table[@id='crudTable']//tbody//tr[1]//td[2]"
            ).text
            print(report_name_text)
            if report_name_text == report_name:
                # Try to find the download option
                wait = WebDriverWait(self.driver, 10)
                download_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//table[@id='crudTable']//tbody//tr[1]//td[9]//a")
                    )
                )
                download_btn.click()
                print("Download option found and clicked")
            else:
                print("Search value does not match")

        except Exception:
            try:
                # If download is not present, check for no data
                no_data = self.driver.find_element(
                    By.XPATH, "//table[@id='crudTable']//tbody//tr[1]//td[9]"
                )
                print("No data available:", no_data.text)

            except Exception:
                print("Neither download option nor no data found")

