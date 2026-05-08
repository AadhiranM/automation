from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SAQRListPage(BasePage):

    URL = "https://beta.digitathya.com/admin/qr-management?reset_filters=1"

    SEARCH_BOX = (By.XPATH, "//input[contains(@placeholder,'Search')]")
    SEARCH_BTN = (By.XPATH, "//button[contains(@class,'search')]")  # adjust if needed

    FIRST_ROW = (By.XPATH, "(//table//tbody/tr)[1]")
    NO_DATA_ROW = (By.XPATH, "//td[contains(@class,'dataTables_empty')]")

    # =========================
    # NAVIGATION
    # =========================

    FIRST_BATCH = (
        By.XPATH,
        "(//table//tbody//tr[1]//td)[4]"
    )

    def get_first_batch_text(self):
        return self.get_text(self.FIRST_BATCH)
    def goto_page(self):
        self.driver.get(self.URL)
        self.wait_for_results()

    # =========================
    # WAIT FOR TABLE
    # =========================
    def wait_for_results(self):
        WebDriverWait(self.driver, 15).until(
            lambda d: d.find_elements(*self.FIRST_ROW)
            or d.find_elements(*self.NO_DATA_ROW)
        )

    # =========================
    # SEARCH (SAME AS MANUFACTURER)
    # =========================
    def search_batch(self, batch):
        self.wait_for_results()

        self.type(self.SEARCH_BOX, batch)
        self.click(self.SEARCH_BTN)

        self.wait_for_results()

    # =========================
    # VALIDATION
    # =========================
    def is_batch_present(self, batch):
        rows = self.driver.find_elements(
            By.XPATH,
            f"//table//tbody//td[contains(text(),'{batch}')]"
        )

        return len(rows) > 0