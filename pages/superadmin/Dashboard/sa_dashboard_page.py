from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage


class SuperAdminDashboard(BasePage):

    # ------------------ TOP BAR ------------------
    DASHBOARD_TITLE = (By.XPATH, "//p[normalize-space()='Dashboard']")

    # ------------------ LEFT MENU ------------------
    MENU_ENQUIRIES = (By.XPATH, "//span[normalize-space()='Enquiries']")
    MENU_MANUFACTURER = (By.XPATH, "//span[normalize-space()='Manufacturer']")
    MENU_QR_MANAGEMENT = (By.XPATH, "//span[normalize-space()='QR Management']")
    MENU_REPORTS = (By.XPATH, "//span[normalize-space()='Reports']")

    # ------------------ PAGE LOAD CHECK ------------------
    def is_loaded(self):
        """Verify dashboard loaded successfully."""
        return self.is_visible(self.DASHBOARD_TITLE)

    # ------------------ NAVIGATION METHODS ------------------

    def goto_enquiries(self):
        """Go to Enquiries module from left menu."""
        self.click(self.MENU_ENQUIRIES)
        return True

    def goto_manufacturer(self):
        self.click(self.MENU_MANUFACTURER)
        return True

    def goto_qr_management(self):
        self.click(self.MENU_QR_MANAGEMENT)
        return True

    def goto_reports(self):
        self.click(self.MENU_REPORTS)
        return True
