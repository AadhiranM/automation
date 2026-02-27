# qr_monitoring_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class QR_Management_Category_Page:
   ## Xpath for all the elements
    Dashboard=(By.XPATH,"//span[@class='nav-name'][normalize-space()='Dashboard']")
    QR_Management= (By.XPATH, "//span[@class='nav-name'][normalize-space()='QR Management']")
    category = (By.XPATH, "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Categories']")
    create_category_button= (By.XPATH,"(//button[@class='btn btn-soft-primary createCategoryFun'])[1]")
    Enter_category=(By.XPATH,"//div[@class='form-group col-sm-12']//input[@placeholder='Enter Category']")
    category_status=(By.XPATH,"//div[@class='form-group col-sm-12']//select[@name='status']")
    save_button=(By.XPATH,"//button[normalize-space()='Save']")
    exit_option=(By.XPATH,"//div[@class='modal-header p-3 bg-primary-subtle']//button[@aria-label='Close']")

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




