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
    filter_by_date=(By.XPATH,"//input[@class='form-control dash-filter-picker input']")
    select_format=(By.XPATH,"//div[@class='input-light select-format-dropdown']//select[@id='format']")
    select_status=(By.XPATH,"//select[@id='idStatus']")
    refresh_btn=(By.XPATH,"//button[@class='btn btn-outline-primary btn-icon waves-effect waves-light reload_btn uicust-active-color uicust-active-border refresh_Btn ']")
    filters_btn=(By.XPATH,"//button[@id='filterToggleBtn']")
    filters_report_name=(By.XPATH,"//div[@class='mb-3']//input[@id='report_name']")
    filters_select_format=(By.XPATH,"//div[@class='h-40 custom-drop-dwn-con ']//select[@id='format']")
    filters_start_date=(By.XPATH,"//input[@id='start_date']")
    filters_end_date=(By.XPATH,"//input[@id='end_date']")
    filters_select_status=(By.XPATH,"//select[@id='status']")
    created_date_range=(By.XPATH,"//input[@id='date_range']")
    filters_apply_btn=(By.XPATH,"//button[normalize-space()='Apply']")
    filters_clr_btn=(By.XPATH,"//button[@id='clear-filter-btn']")
    create_Batch_status_report=(By.XPATH,"//select[@id='schedule_report_name']")
    create_select_format=(By.XPATH,"//select[@id='schedule_report_name']")
    create_choose_mail_receiving_duration=(By.XPATH,"//select[@id='mail_send_at']")
    create_select_duration=(By.XPATH,"//select[@id='duration']")



