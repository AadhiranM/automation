import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class QR_Management_QR_m_filters:
    ## Xpath for all the elements
    Qr_management = (By.XPATH, "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='QR Management']")
    reset_btn=(By.XPATH,"//button[contains(@class,'btn btn-outline-primary btn-icon waves-effect waves-light reload_btn uicust-active-color uicust-active-border refresh_Btn')]")
    filters_btn=(By.XPATH,"//button[@id='filterToggleBtn']")
    filters_prd_name=(By.XPATH,"//input[@id='product_name']")
    filters_mftr_date=(By.XPATH,"//input[@id='manufacturing_date']")
    filters_exp_date=(By.XPATH,"//input[@id='expiry_date']")
    filters_apply_btn=(By.XPATH,"//button[normalize-space()='Apply']")
    clear_filter=(By.XPATH,"//button[@id='clear-filter-btn']")
    filter_product_name=(By.XPATH,"//input[@id='product_name']")
    search_field=(By.XPATH,"//input[@id='search-vale']")
    search_btn=(By.XPATH,"//button[@id='search-btn']")
    table_rows=(By.XPATH,"//table[@id='crudTable']//tbody//tr")
    table_column=(By.XPATH,"//table[@id='crudTable']//tbody//tr//td")
    table_xpath=(By.XPATH,"//table[@id='crudTable']")
    status_drp=(By.XPATH,"//select[@id='idStatus']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---------------- Actions ----------------
    def Click_Qr_management(self):
        self.driver.find_element(*self.Qr_management).click()

    def Click_reset_btn(self):
        self.driver.find_element(*self.reset_btn).click()

    def Enter_search_field(self,search_value):
        self.driver.find_element(*self.search_field).send_keys(search_value)

    def Click_search_btn(self):
        self.driver.find_element(*self.search_btn).click()

    def select_status_drp(self,select_status):
        drpdwn_status=Select(self.driver.find_element(*self.status_drp))
        drpdwn_status.select_by_visible_text(select_status)

    def getNoOfRows(self):
        return len(self.driver.find_elements(*self.table_rows))

    def getNoOfColumns(self):
        return len(self.driver.find_elements(*self.table_column))

    def search_product(self, search_value):
        flag = False
        for r in range(1, self.getNoOfRows() + 1):
            table = self.driver.find_element(*self.table_xpath)
            time.sleep(2)

            # Read both columns
            product_name = table.find_element(By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[2]").text.strip()
            batch_no = table.find_element(By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[3]").text.strip()

            print(product_name)
            print(batch_no)
            # Match if search_value equals either product_name or batch_no
            if search_value == product_name or search_value == batch_no:
                flag = True
                break
        return flag

    def Click_filter_button(self):
        self.driver.find_element(*self.filters_btn).click()

    def Enter_filter_prd_name(self,product_name):
        self.driver.find_element(*self.filter_product_name).clear()
        self.driver.find_element(*self.filter_product_name).send_keys(product_name)

    def Click_filters_apply_btn(self):
        self.driver.find_element(*self.filters_apply_btn).click()

    def Click_manufacturer_date(self):
        self.driver.find_element(*self.filters_mftr_date).click()

    def Click_expiry_date(self):
        self.driver.find_element(*self.filters_exp_date).click()

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

    def set_manufacturing_date(self, date_string):
        self.wait.until(EC.element_to_be_clickable(self.filters_mftr_date)).click()
        self.select_date(date_string)

    def set_expiry_date(self, date_string):
        self.wait.until(EC.element_to_be_clickable(self.filters_exp_date)).click()
        self.select_date(date_string)


