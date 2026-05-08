import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class user_create:
    Dashboard = (By.XPATH, "//span[@class='nav-name'][normalize-space()='Dashboard']")
    user_management_opt=(By.XPATH,"//span[normalize-space()='User Management']")
    users=(By.XPATH,"//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Users']")
    create=(By.XPATH,"//a[normalize-space()='Create']")
    username=(By.XPATH,"//input[@placeholder='Enter User Name']")
    Email=(By.XPATH,"//input[@placeholder='Enter Email ID']")
    Role_drpdown=(By.XPATH,"//div[@class='choices__inner']")
    Role_input=(By.XPATH,"//input[@name='search_terms']")
    select_status=(By.XPATH,"//select[@name='status']")
    Mobile_number=(By.XPATH,"//input[@placeholder='Please enter a valid 10-digit mobile number.']")
    password=(By.XPATH,"//input[@id='masked_password']")
    submit_btn=(By.XPATH,"//button[normalize-space()='Submit']")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ================= NAVIGATION =================
    # def Click_Dashboard(self):
    #     self.driver.find_element(*self.Dashboard).click()
    #
    # def Click_User_management(self):
    #     self.driver.find_element(*self.user_management_opt).click()
    #
    # def Click_users(self):
    #     self.driver.find_element(*self.users).click()
    #
    # def Click_create(self):
    #     self.driver.find_element(*self.create).click()
    #
    # def Enter_username(self,user_name):
    #     self.driver.find_element(*self.username).send_keys(user_name)
    #
    # def Enter_Email(self,Email):
    #     self.driver.find_element(*self.Email).send_keys(Email)
    #
    # def select_Role_drpdown(self):
    #     self.driver.find_element(*self.Role_drpdown).click()
    #
    # def Enter_Role_input(self,select_Role):
    #     self.driver.find_element(*self.Role_input).send_keys(select_Role)
    #     time.sleep(1)
    #     self.driver.find_element(*self.Role_input).send_keys(Keys.ENTER)
    #
    # def Choose_select_status(self, select_status):
    #     drpdwn = Select(self.driver.find_element(*self.select_status))
    #     drpdwn.select_by_visible_text(select_status)
    #
    # def Enter_Mobile_number(self,Mobile_number):
    #     self.driver.find_element(*self.Mobile_number).send_keys(Mobile_number)
    #
    # def Enter_password(self,password):
    #     self.driver.find_element(*self.password).send_keys(password)
    #
    # def Click_submit_btn(self):
    #     submit = WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable(self.submit_btn)
    #     )
    #     # Scroll to element
    #     self.driver.execute_script("arguments[0].scrollIntoView(true);", submit)
    #     time.sleep(1)
    #
    #     # Click using JS (very reliable)
    #     self.driver.execute_script("arguments[0].click();", submit)
    #
    #     # Scroll back to top to see popup
    #     self.driver.execute_script("window.scrollTo(0, 0);")
    #
    def Click_Dashboard(self):
        self.wait.until(
            EC.element_to_be_clickable(self.Dashboard)
        ).click()

    def Click_User_management(self):
        self.wait.until(
            EC.element_to_be_clickable(self.user_management_opt)
        ).click()

    def Click_users(self):
        self.wait.until(
            EC.element_to_be_clickable(self.users)
        ).click()

    def Click_create(self):
        self.wait.until(
            EC.element_to_be_clickable(self.create)
        ).click()

    def Enter_username(self, user_name):
        self.wait.until(
            EC.visibility_of_element_located(self.username)
        ).send_keys(user_name)

    def Enter_Email(self, Email):
        self.wait.until(
            EC.visibility_of_element_located(self.Email)
        ).send_keys(Email)

    def select_Role_drpdown(self):
        self.wait.until(
            EC.element_to_be_clickable(self.Role_drpdown)
        ).click()

    def Enter_Role_input(self, select_Role):
        role_input = self.wait.until(
            EC.visibility_of_element_located(self.Role_input)
        )
        role_input.send_keys(select_Role)
        time.sleep(1)
        role_input.send_keys(Keys.ENTER)

    def Choose_select_status(self, select_status):
        drpdwn = Select(
            self.wait.until(
                EC.presence_of_element_located(self.select_status)
            )
        )
        drpdwn.select_by_visible_text(select_status)

    def Enter_Mobile_number(self, Mobile_number):
        self.wait.until(
            EC.visibility_of_element_located(self.Mobile_number)
        ).send_keys(Mobile_number)

    def Enter_password(self, password):
        self.wait.until(
            EC.visibility_of_element_located(self.password)
        ).send_keys(password)

    def Click_submit_btn(self):
        submit = self.wait.until(
            EC.element_to_be_clickable(self.submit_btn)
        )

        # Scroll to element
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit)
        time.sleep(1)

        # JS click (stable)
        self.driver.execute_script("arguments[0].click();", submit)

        # Scroll back
        self.driver.execute_script("window.scrollTo(0, 0);")
