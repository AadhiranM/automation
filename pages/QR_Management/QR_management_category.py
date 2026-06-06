# qr_monitoring_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import calendar

class QR_Management_Category_Page:
   ## Xpath for all the elements
    Dashboard=(By.XPATH,"//span[@class='nav-name'][normalize-space()='Dashboard']")
    QR_Management= (By.XPATH, "//span[@class='nav-name'][normalize-space()='QR Management']")
    category = (By.XPATH, "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Categories']")
    create_category_button= (By.XPATH,"(//button[@class='btn btn-soft-primary createCategoryFun'])[1]")
    Enter_category=(By.XPATH,"//div[@class='form-group col-sm-12']//input[@placeholder='Enter Category Name']")
    category_status=(By.XPATH,"//div[@class='form-group col-sm-12']//select[@name='status']")
    save_button=(By.XPATH,"//button[normalize-space()='Save']")
    exit_option=(By.XPATH,"//div[@class='modal-header p-3 bg-primary-subtle']//button[@aria-label='Close']")

   #filters
    search_input_field=(By.XPATH,"//input[@id='search-vale']")
    calender_date_range=(By.XPATH,"//input[@id='datepicker-range']")
    select_status=(By.XPATH,"//select[@id='idStatus']")

    #filter_toggle
    filter_toggle_btn=(By.XPATH,"//button[@id='filterToggleBtn']")
    filter_toggle_category_field=(By.XPATH,"//input[@id='category_name']")
    filter_toggle_date_range=(By.XPATH,"//input[@id='date_range']")
    filter_toggle_status=(By.XPATH,"//select[@id='status']")
    filter_toggle_apply_btn=(By.XPATH,"//button[normalize-space()='Apply']")

    #actions and edit buttons
    actions_icon=(By.XPATH,"//i[@class='ri-more-fill align-middle']")
    edit_opt=(By.XPATH,"//a[@role='button']")
    edit_category_name=(By.XPATH,"//div[@class='form-group col-sm-12']//input[@name='category_name']")
    edit_status=(By.XPATH,"//select[@id='createcategoryStatus']")
    edit_update_btn=(By.XPATH,"//button[normalize-space()='Update']")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Actions
    def Click_Dashboard(self):
        self.driver.find_element(*self.Dashboard).click()

    def Click_QR_management(self):
        self.driver.find_element(*self.QR_Management).click()

    def click_category(self):
        self.driver.find_element(*self.category).click()

    def click_create_category_button(self):
        self.driver.find_element(*self.create_category_button).click()

    def Enter_category_value(self,category):
        self.driver.find_element(*self.Enter_category).clear()
        self.driver.find_element(*self.Enter_category).send_keys(category)

    def click_category_status(self,value):
        drp=Select(self.driver.find_element(*self.category_status))
        drp.select_by_visible_text(value)

    def click_save_button(self):
        self.driver.find_element(*self.save_button).click()

    def Click_exit_option(self):
        self.driver.find_element(*self.exit_option).click()

    def Enter_search_field(self,search_value):
        self.driver.find_element(*self.search_input_field).clear()
        time.sleep(1)
        self.driver.find_element(*self.search_input_field).send_keys(search_value)

    def Click_calender_date_range(self):
        self.driver.find_element(*self.calender_date_range).click()

    def Enter_select_status(self,status_value):
        drp=Select(self.driver.find_element(*self.select_status))
        drp.select_by_visible_text(status_value)

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

    def Click_filter_toggle(self):
        self.driver.find_element(*self.filter_toggle_btn).click()

    def Enter_filter_toggle_category_field(self,category_name):
        self.driver.find_element(*self.filter_toggle_category_field).clear()
        time.sleep(1)
        self.driver.find_element(*self.filter_toggle_category_field).send_keys(category_name)


    def Click_filter_toggle_date_range(self):
        self.driver.find_element(*self.filter_toggle_date_range).click()

    def select_filter_toggle_status(self,status_value):
        drp=Select(self.driver.find_element(*self.filter_toggle_status))
        drp.select_by_visible_text(status_value)

    def Click_filter_toggle_apply_btn(self):
        self.driver.find_element(*self.filter_toggle_apply_btn).click()

    def search_product(self,category_name):
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
                search_name = self.driver.find_element(
                    By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[2]"
                ).text.strip()
                active_status = self.driver.find_element(
                    By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[3]"
                ).text.strip()
                time.sleep(1)
                print(search_name)
                print(active_status)
                if search_name == category_name:
                    flag = True
                    break

        except Exception as e:
            print(f"Exception in searching product: {e}")
            flag = False
        return flag

    def click_actions_icon(self):
        self.driver.find_element(*self.actions_icon).click()

    def click_edit_opt(self):
        self.driver.find_element(*self.edit_opt).click()

    def enter_edit_category_name(self,edit_category_name):
        self.driver.find_element(*self.edit_category_name).clear()
        self.driver.find_element(*self.edit_category_name).send_keys(edit_category_name)

    def select_edit_status(self,edit_status):
        drp=Select(self.driver.find_element(*self.edit_status))
        drp.select_by_visible_text(edit_status)

    def click_edit_update_btn(self):
        self.driver.find_element(*self.edit_update_btn).click()



