from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import calendar
from selenium.webdriver.common.action_chains import ActionChains

class QR_Management_variants_Page:
   ## Xpath for all the elements
    variants= (By.XPATH, "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Variants']")
    create_button= (By.XPATH,"//a[normalize-space()='Create Variants']")
    category_option=(By.XPATH,"//span[@role='combobox']")
    category_field=(By.XPATH,"//input[@placeholder='Enter Category Name']")
    category_Entered_name=(By.XPATH,"//li[@class='select2-results__option select2-results__option--selectable select2-results__option--highlighted']")
    variants_type_field=(By.XPATH,"//input[@placeholder='Enter Variant Type']")
    variants_value_field=(By.XPATH,"//input[@placeholder='Enter Variant Value']")
    save_variants_button=(By.XPATH,"//button[normalize-space()='Save Variants']")

   #filter and edit
    refresh_btn=(By.XPATH,"//button[@class='btn btn-outline-primary btn-icon waves-effect waves-light reload_btn uicust-active-color uicust-active-border refresh_Btn ']")
    search_category_name=(By.XPATH,"//input[@id='search-vale']")
    actions_icon=(By.XPATH,"//i[@class='ri-more-fill align-middle']")
    edit_opt=(By.XPATH,"//span[normalize-space()='Edit']")
    edit_variant_type=(By.XPATH,"//input[@placeholder='Enter Variant Type']")
    edit_variant_value=(By.XPATH,"//input[@placeholder='Enter Variant Value']")
    update_btn=(By.XPATH,"//button[contains(text(),'Update')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Actions
    def Click_variants(self,):
        self.driver.find_element(*self.variants).click()

    def click_create_button(self):
        self.driver.find_element(*self.create_button).click()

    def click_category_option(self):
        self.driver.find_element(*self.category_option).click()

    def Enter_category_field(self,category_name):
        self.driver.find_element(*self.category_field).clear()
        self.driver.find_element(*self.category_field).send_keys(category_name)

    def Click_Category_Entered_name(self):
        self.driver.find_element(*self.category_Entered_name).click()

    def Enter_variants_type_field(self,variant_type):
        self.driver.find_element(*self.variants_type_field).clear()
        self.driver.find_element(*self.variants_type_field).send_keys(variant_type)

    def Enter_variants_value_field(self, variant_value):
        self.driver.find_element(*self.variants_value_field).clear()
        self.driver.find_element(*self.variants_value_field).send_keys(variant_value)

    def click_save_variants_button(self):
        self.driver.find_element(*self.save_variants_button).click()


    def search_product(self,search_category_name):
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
                    By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[1]"
                ).text.strip()
                time.sleep(1)
                print(search_name)
                if search_name == search_category_name:
                    flag = True
                    break

        except Exception as e:
            print(f"Exception in searching product: {e}")
            flag = False
        return flag

    def click_refresh_btn(self):
        self.driver.find_element(*self.refresh_btn).click()


    def Enter_search_category_name(self, search_category_name):
        search = self.driver.find_element(*self.search_category_name)
        search.clear()
        search.send_keys(search_category_name)
        search.send_keys(Keys.ENTER)

    def click_actions_icon(self):
        self.driver.find_element(*self.actions_icon).click()

    def click_edit_opt(self):
        self.driver.find_element(*self.edit_opt).click()

    def Enter_edit_variant_type(self,edit_variant_type):
        self.driver.find_element(*self.edit_variant_type).clear()
        self.driver.find_element(*self.edit_variant_type).send_keys(edit_variant_type)

    def Enter_edit_variant_value(self,edit_variant_value):
        self.driver.find_element(*self.edit_variant_value).clear()
        self.driver.find_element(*self.edit_variant_value).send_keys(edit_variant_value)


    def click_update_btn(self):
        update_btn = self.wait.until(
            EC.presence_of_element_located(self.update_btn)
        )
        # Scroll element into center
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            update_btn
        )
        time.sleep(1)
        # Move mouse to element
        ActionChains(self.driver).move_to_element(update_btn).perform()
        update_btn.click()






