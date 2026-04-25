import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SAProductCreateChildPage(BasePage):

    CHILD_TAB = (By.XPATH, "//a[normalize-space()='Child SKU']")
    CONTINUE_BTN = (By.ID, "nextButton")
    TYPE_1 = (By.XPATH,
              "(//div[contains(@class,'tab-pane') and contains(@class,'active')]//div[contains(@class,'choices__inner')])[1]")
    TYPE_2 = (By.XPATH,
              "(//div[contains(@class,'tab-pane') and contains(@class,'active')]//div[contains(@class,'choices__inner')])[2]")

    VALUE_1 = (By.XPATH,
               "(//div[contains(@class,'tab-pane') and contains(@class,'active')]//div[contains(@class,'choices__inner')])[3]")
    VALUE_2 = (By.XPATH,
               "(//div[contains(@class,'tab-pane') and contains(@class,'active')]//div[contains(@class,'choices__inner')])[4]")
    # -------------------------
    def open_child_tab(self):
        self.click(self.CHILD_TAB)

        # wait tab active
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[contains(@class,'active') and normalize-space()='Child SKU']"
            ))
        )

        # 🔥 WAIT FOR DROPDOWN CONTAINER (REAL FIX)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class,'choices')]"
            ))
        )

        # 🔥 EXTRA WAIT (YOUR APP NEEDS THIS)
        time.sleep(3)

    def select_variant(self):
        self.select_dropdown(self.TYPE_1, "Type_xikng")

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[@role='option' and contains(.,'Type_')]"
            ))
        )

        self.select_dropdown(self.TYPE_2, "Type_xikngr")

        self.select_dropdown(self.VALUE_1, "value_iwojq")
        time.sleep(1)

        self.select_dropdown(self.VALUE_2, "value_iwojd")

    # -------------------------
    def go_to_video(self):
        self.click(self.CONTINUE_BTN)