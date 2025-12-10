# pages/superadmin/Enquiries/sa_enquiry_list_page.py

import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker


class SAEnquiryListPage(BasePage):

    # ----------------- SEARCH -----------------
    SEARCH_BOX = (By.ID, "search-vale")

    # ----------------- MENU -----------------
    ENQUIRIES_MENU = (By.XPATH, "//span[normalize-space()='Enquiries']")

    # ----------------- TABLE -----------------
    FIRST_ROW = (By.XPATH, "(//table[contains(@class,'table')]//tbody/tr)[1]")
    NO_DATA_ROW = (By.XPATH, "//td[contains(@class,'dataTables_empty')]")
    CREATED_AT_COL = (By.XPATH, "//table[contains(@class,'table')]//tbody/tr/td[8]")

    # ----------------- ACTION MENU LOCATORS -----------------
    FIRST_ROW_ACTION_BTN = (
        By.XPATH,
        "//table[contains(@class,'table')]//tbody/tr[1]//button[contains(@class,'dropdown')]"
    )

    ACTION_VIEW = (By.XPATH, "//a[normalize-space()='View']")
    ACTION_EDIT = (By.XPATH, "//a[normalize-space()='Edit']")
    ACTION_ASSIGN = (By.XPATH, "//button[contains(text(),'Assign Internal User')]")
    ACTION_UNASSIGN = (By.XPATH, "//a[contains(text(),'Un-assign')]")
    ACTION_SEND_EMAIL = (By.XPATH, "//a[normalize-space()='Send Email']")
    ACTION_FOLLOWUP = (By.XPATH, "//a[normalize-space()='Follow Up']")

    # ----------------- DATE FILTERS -----------------
    INLINE_CREATED_AT = (By.XPATH, "//input[@placeholder='Filter by : Created At']")
    FILTER_PANEL_BTN = (By.ID, "filterToggleBtn")
    PANEL_DATE_RANGE = (By.ID, "date_range")

    APPLY_BTN = (By.XPATH, "//button[normalize-space()='Apply']")
    CLEAR_BTN = (By.XPATH, "//button[normalize-space()='Clear Filter']")
    FILTER_CLOSE_ICON = (By.CSS_SELECTOR, "div.offcanvas-header button.close")

    # ----------------- NAVIGATION -----------------
    def goto_page(self):
        """Navigate to enquiry list."""
        try:
            self.click(self.ENQUIRIES_MENU)
        except:
            pass

        self.driver.get("https://beta.digitathya.com/admin/enquires?reset_filters=1")
        self.wait_for_results()

    def wait_for_results(self):
        """Wait until table row OR 'no data' message is visible."""
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_elements(*self.FIRST_ROW) or d.find_elements(*self.NO_DATA_ROW)
        )

    # ----------------- SEARCH -----------------
    def search(self, text):
        self.type(self.SEARCH_BOX, text)
        try:
            self.driver.find_element(*self.SEARCH_BOX).send_keys("\n")
        except:
            pass

    # ----------------- INLINE CALENDAR -----------------
    def open_inline_calendar(self):
        self.click(self.INLINE_CREATED_AT)
        time.sleep(0.25)

    # ----------------- FILTER PANEL -----------------
    def open_filter_panel(self):
        self.click(self.FILTER_PANEL_BTN)
        time.sleep(0.4)

    def close_filter_panel(self):
        """Safely closes the offcanvas panel."""
        try:
            # already closed
            if not self.driver.find_elements(By.CSS_SELECTOR, "div.offcanvas.show"):
                return True

            if self.driver.find_elements(*self.FILTER_CLOSE_ICON):
                try:
                    self.click(self.FILTER_CLOSE_ICON)
                    return True
                except:
                    pass

            # ESC fallback
            self.driver.execute_script(
                "document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));"
            )
            time.sleep(0.1)
            return True
        except:
            return True

    # ----------------- INLINE DATE FILTER -----------------
    def filter_inline_created_at(self, start, end):
        self.open_inline_calendar()
        picker = FlatpickrRangePicker(self.driver)

        try:
            ok = picker.select_range(start, end)
        except Exception:
            ok = False

        if not ok:
            return True  # range disabled → no results expected

        time.sleep(0.25)
        return False

    # ----------------- PANEL DATE FILTER -----------------
    def filter_panel_created_at(self, start, end):
        self.open_filter_panel()
        picker = FlatpickrRangePicker(self.driver)

        try:
            self.click(self.PANEL_DATE_RANGE)
            time.sleep(0.25)
        except:
            self.close_filter_panel()
            return True

        try:
            ok = picker.select_range(start, end)
        except Exception:
            ok = False

        if not ok:
            self.close_filter_panel()
            return True

        try:
            self.click(self.APPLY_BTN)
        except:
            pass

        self.close_filter_panel()
        return False

    # ----------------- ACTION MENU METHODS -----------------
    def open_action_menu(self):
        self.click(self.FIRST_ROW_ACTION_BTN)

    def click_view(self):
        self.click(self.ACTION_VIEW)

    def click_edit(self):
        self.click(self.ACTION_EDIT)

    def click_assign(self):
        self.click(self.ACTION_ASSIGN)

    def click_unassign(self):
        self.click(self.ACTION_UNASSIGN)

    def click_send_email(self):
        self.click(self.ACTION_SEND_EMAIL)

    def click_followup(self):
        self.click(self.ACTION_FOLLOWUP)

    # ----------------- TABLE HELPERS -----------------
    def has_no_results(self):
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_elements(*self.NO_DATA_ROW) or d.find_elements(*self.FIRST_ROW)
            )
            return bool(self.driver.find_elements(*self.NO_DATA_ROW))
        except:
            return False

    def is_row_present(self):
        return bool(self.driver.find_elements(*self.FIRST_ROW))

    def get_all_created_dates(self):
        """Returns Created At column values as Python date objects."""
        rows = self.driver.find_elements(*self.CREATED_AT_COL)
        result = []
        for r in rows:
            try:
                dt = datetime.strptime(r.text.strip(), "%d %b %Y %I:%M %p").date()
                result.append(dt)
            except:
                pass
        return result

    def has_disabled_future_dates(self):
        """Used for negative tests to confirm future days are disabled."""
        try:
            # open inline calendar if needed
            if not self.driver.find_elements(By.CSS_SELECTOR, "div.flatpickr-calendar.open"):
                self.open_inline_calendar()

            time.sleep(0.12)
            disabled = self.driver.find_elements(By.CSS_SELECTOR, "span.flatpickr-day.flatpickr-disabled")

            # Close calendar
            try:
                self.driver.execute_script(
                    "document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));"
                )
            except:
                pass

            return len(disabled) > 0
        except:
            return False
