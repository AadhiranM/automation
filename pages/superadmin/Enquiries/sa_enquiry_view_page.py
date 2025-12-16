# pages/superadmin/Enquiries/sa_enquiry_view_page.py

from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage


class SAEnquiryViewPage(BasePage):

    # View page fields (always in 2nd <td> cell)
    NAME = (By.XPATH, "//strong[text()='Name:']/ancestor::tr/td[2]/span")
    PHONE = (By.XPATH, "//strong[text()='Phone:']/ancestor::tr/td[2]/span")
    EMAIL = (By.XPATH, "//strong[text()='Business Email:']/ancestor::tr/td[2]/span")
    COMPANY = (By.XPATH, "//strong[text()='Company:']/ancestor::tr/td[2]/span")
    STATUS = (By.XPATH, "//strong[text()='Status:']/ancestor::tr/td[2]/span")
    MESSAGE = (By.XPATH, "//strong[text()='Message:']/ancestor::tr/td[2]/span")

    EDIT_BUTTON = (By.XPATH, "//a[normalize-space()='Edit']")

    def wait_until_loaded(self):
        """Ensures that essential fields are visible before assertions."""
        self.is_visible(self.NAME)
        self.is_visible(self.EMAIL)
        self.is_visible(self.STATUS)

    def click_edit(self):
        self.click(self.EDIT_BUTTON)



