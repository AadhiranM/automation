from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage


class SAManufacturerViewPage(BasePage):

    COMPANY_NAME = (By.XPATH, "//label[text()='Company Name']/following-sibling::div")
    EMAIL = (By.XPATH, "//label[text()='Business Email']/following-sibling::div")
    STATUS = (By.XPATH, "//label[text()='Status']/following-sibling::div")

