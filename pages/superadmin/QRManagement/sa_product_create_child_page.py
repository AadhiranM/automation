import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.common.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains

class SAProductCreateChildPage(BasePage):

    CHILD_TAB = (By.XPATH, "//a[normalize-space()='Child SKU']")
    CONTINUE_BTN = (
        By.XPATH,
        "//div[@id='pill-justified-variant-1' and contains(@class,'active')]//button[contains(.,'Continue to Video Details')]"
    )

    # ALL DROPDOWNS (DYNAMIC)
    ALL_DROPDOWNS = (
        By.XPATH,
        "//div[contains(@class,'tab-pane') and contains(@class,'active')]//div[contains(@class,'choices__inner')]"
    )

    # -------------------------
    def open_child_tab(self):
        self.click(self.CHILD_TAB)

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[contains(@class,'active') and normalize-space()='Child SKU']"
            ))
        )

        # wait All dropdowns
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located(self.ALL_DROPDOWNS)
        )


        time.sleep(2)

    # -------------------------
    from selenium.webdriver.common.action_chains import ActionChains

    def select_all_variants(self):
        wait = WebDriverWait(self.driver, 15)

        # Get ALL dropdown containers
        dropdowns = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'tab-pane') and contains(@class,'active')]//div[contains(@class,'choices__inner')]"
        )

        print(f"Total dropdown elements: {len(dropdowns)}")

        # Each column has 2 dropdowns (Type + Value)
        # So process in pairs
        i = 0
        while i < len(dropdowns):

            # =========================
            # 🔹 SELECT TYPE
            # =========================
            dropdowns = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'tab-pane') and contains(@class,'active')]//div[contains(@class,'choices__inner')]"
            )

            type_dropdown = dropdowns[i]

            # self.driver.execute_script("arguments[0].scrollIntoView(true);", type_dropdown)
            # time.sleep(1)
            #
            # type_dropdown.click()

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                type_dropdown
            )

            wait.until(
                lambda d: type_dropdown.is_displayed() and type_dropdown.is_enabled()
            )

            time.sleep(0.5)

            try:
                type_dropdown.click()
            except:
                self.driver.execute_script(
                    "arguments[0].click();",
                    type_dropdown
                )
            time.sleep(1)

            type_options = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'choices__list--dropdown')]//div[@role='option']"
            )

            valid_type = [
                o for o in type_options
                if o.text.strip() and "Select" not in o.text and "disabled" not in o.get_attribute("class")
            ]

            if not valid_type:
                print(f"No TYPE options at index {i}")
                break

            selected_type = valid_type[0].text
            valid_type[0].click()

            print(f"Type Selected: {selected_type}")
            time.sleep(2)

            # =========================
            # 🔹 SELECT VALUE (NEXT INDEX)
            # =========================
            dropdowns = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'tab-pane') and contains(@class,'active')]//div[contains(@class,'choices__inner')]"
            )

            # value dropdown will be next element
            if i + 1 >= len(dropdowns):
                break

            value_dropdown = dropdowns[i + 1]

            # self.driver.execute_script("arguments[0].scrollIntoView(true);", value_dropdown)
            # time.sleep(1)
            #
            # value_dropdown.click()
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                value_dropdown
            )

            wait.until(
                lambda d: value_dropdown.is_displayed() and value_dropdown.is_enabled()
            )

            time.sleep(0.5)

            try:
                value_dropdown.click()
            except:
                self.driver.execute_script(
                    "arguments[0].click();",
                    value_dropdown
                )
            time.sleep(1)

            value_options = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'choices__list--dropdown')]//div[@role='option']"
            )

            valid_value = [
                o for o in value_options
                if o.text.strip() and "Select" not in o.text and "disabled" not in o.get_attribute("class")
            ]

            if not valid_value:
                print(f" No VALUE options at index {i + 1}")
                break

            selected_value = valid_value[0].text
            valid_value[0].click()

            print(f" Value Selected: {selected_value}")
            time.sleep(2)

            # move to next column (skip 2)
            i += 2

    # -------------------------
    def go_to_video(self):

        btn = self.driver.find_element(*self.CONTINUE_BTN)

        print("Displayed :", btn.is_displayed())
        print("Enabled   :", btn.is_enabled())

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            btn
        )

        btn.click()