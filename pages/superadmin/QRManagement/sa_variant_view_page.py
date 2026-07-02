from selenium.webdriver.common.by import By

from pages.common.base_page import BasePage


class SAVariantViewPage(BasePage):

    VARIANT_TYPE_TEXT = (
        By.XPATH,
        "//table//tbody/tr[1]/td[1]"
    )

    VARIANT_VALUE_TEXT = (
        By.XPATH,
        "//table//tbody/tr[1]/td[2]"
    )

    def is_view_page_opened(self):

        current_url = self.driver.current_url.lower()

        return (
            "show" in current_url
            or "/view/" in current_url
            or "/show/" in current_url
        )

    def get_variant_type(self):

        return self.driver.find_element(
            *self.VARIANT_TYPE_TEXT
        ).text.strip()

    def get_variant_value(self):

        return self.driver.find_element(
            *self.VARIANT_VALUE_TEXT
        ).text.strip()