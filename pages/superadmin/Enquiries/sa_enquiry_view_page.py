from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class SAEnquiryViewPage(BasePage):

    NAME = (
        By.XPATH,
        "//strong[contains(text(),'Name')]/parent::td/following-sibling::td"
    )

    EMAIL = (
        By.XPATH,
        "//strong[contains(text(),'Business Email')]/parent::td/following-sibling::td"
    )

    COMPANY = (
        By.XPATH,
        "//strong[contains(text(),'Company')]/parent::td/following-sibling::td"
    )

    STATUS = (
        By.XPATH,
        "//strong[contains(text(),'Status')]/parent::td/following-sibling::td"
    )

    EDIT_BUTTON = (
        By.XPATH,
        "//a[contains(.,'Edit')]"
    )

    def wait_until_loaded(self):

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                self.NAME
            )
        )

    def get_name(self):
        return self.get_text(self.NAME).strip()

    def get_email(self):
        return self.get_text(self.EMAIL).strip()

    def get_company(self):
        return self.get_text(self.COMPANY).strip()

    def get_status(self):
        return self.get_text(self.STATUS).strip()