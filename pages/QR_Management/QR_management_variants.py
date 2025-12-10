from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class QR_Management_variants_Page:
   ## Xpath for all the elements
    # QR_Management= (By.XPATH, "//span[@class='nav-name'][normalize-space()='QR Management']")
    variants= (By.XPATH, "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Variants']")
    create_button= (By.XPATH,"//a[normalize-space()='Create']")
    category_option=(By.XPATH,"//span[@role='combobox']")
    category_field=(By.XPATH,"//input[@placeholder='Enter Category Name']")
    category_Entered_name=(By.XPATH,"//li[@class='select2-results__option select2-results__option--selectable select2-results__option--highlighted']")
    variants_type_field=(By.XPATH,"//input[@placeholder='Enter Variant Type']")
    variants_value_field=(By.XPATH,"//input[@placeholder='Enter Variant Value']")
    save_variants_button=(By.XPATH,"//button[normalize-space()='Save Variants']")


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




