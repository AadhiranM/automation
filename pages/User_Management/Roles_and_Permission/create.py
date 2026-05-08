import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Roles_and_permission_create:
    Dashboard = (By.XPATH, "//span[@class='nav-name'][normalize-space()='Dashboard']")
    user_management_opt=(By.XPATH,"//span[normalize-space()='User Management']")
    roles_and_permission=(By.XPATH,"//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Roles & Permissions']")
    create=(By.XPATH,"//a[normalize-space()='Create']")
    Role_name=(By.XPATH,"//input[@placeholder='Enter Role Name']")
    user_type_dropdown=(By.XPATH,"//span[@id='select2-idSelectuser-container']")
    user_type_input=(By.XPATH,"//input[@aria-label='Search']")

    status=(By.XPATH,"//select[@id='idSelectstatus']")
    submit_btn=(By.XPATH,"//button[normalize-space()='Submit']")
    check_all=(By.XPATH,"//div[@class='d-flex justify-content-between align-items-center mb-3 permission_field']//button[@id='check-all']")



    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ================= NAVIGATION =================
    def Click_Dashboard(self):
        self.driver.find_element(*self.Dashboard).click()

    def Click_User_management(self):
        self.driver.find_element(*self.user_management_opt).click()

    def Click_roles_and_permission(self):
        self.driver.find_element(*self.roles_and_permission).click()

    def Click_create(self):
        self.driver.find_element(*self.create).click()

    def Enter_role_name(self,Role_name):
        self.driver.find_element(*self.Role_name).send_keys(Role_name)


    def select_user_type(self, user_type):
        # click dropdown
        self.wait.until(
            EC.element_to_be_clickable(self.user_type_dropdown)
        ).click()

        # enter value in search field
        search_box = self.wait.until(
            EC.visibility_of_element_located(self.user_type_input)
        )

        search_box.send_keys(user_type)

        # select option
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//li[contains(text(),'{user_type}')]")
            )
        ).click()

    # def select_status(self,select_status):
    #     self.driver.find_element(*self.status).send_keys(select_status)

    def select_status(self, select_status):
        element = self.wait.until(
            EC.element_to_be_clickable(self.status)
        )

        Select(element).select_by_visible_text(select_status)

    def select_check_all_btn(self):
        self.driver.find_element(*self.check_all).click()


    def Click_submit_btn(self):
        submit = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.submit_btn)
        )

        # Scroll to element
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit)
        time.sleep(1)

        # Click using JS (very reliable)
        self.driver.execute_script("arguments[0].click();", submit)

        # Scroll back to top to see popup
        self.driver.execute_script("window.scrollTo(0, 0);")

