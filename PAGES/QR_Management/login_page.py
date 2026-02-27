import unittest
import time
import datetime
import openpyxl
# from HtmlTestRunner import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Set up the WebDriver using webdriver-manager to handle GeckoDriver
service=Service(GeckoDriverManager().install())

class Loginpage:
    def __init__(self, driver):
        self.driver=driver
        self.driver.maximize_window()

    def setUserName(self,username):
        self.driver.find_element(By.XPATH,"//input[@id='username']").clear()
        self.driver.find_element(By.XPATH,"//input[@id='username']").send_keys(username)

    def setPassword(self,password):
        self.driver.find_element(By.XPATH,"//input[@id='password-input']").clear()
        self.driver.find_element(By.XPATH,"//input[@id='password-input']").send_keys(password)

    def clickLogin(self):
        self.driver.find_element(By.XPATH,"//button[normalize-space()='Login']").click()

    def clickLogout(self):
        self.driver.find_element(By.XPATH,"//span[@class='text-start ms-xl-2']").click()
        self.driver.find_element(By.XPATH,"//span[normalize-space()='Logout']").click()


