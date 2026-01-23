import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Generate_reports_page:
    Reports_tab=(By.XPATH,"//span[normalize-space()='Reports']")
    schedule_report=(By.XPATH,"//ul[@class='collapse-menu show']//a[@class='collapse-sublink active']")
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
    

