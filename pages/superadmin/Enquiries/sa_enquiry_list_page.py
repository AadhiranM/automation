from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker
import time


class SAEnquiryListPage(BasePage):

    SEARCH_BOX = (By.ID, "search-vale")
    ENQUIRIES_MENU = (By.XPATH, "//span[normalize-space()='Enquiries']")
    FIRST_ROW = (By.XPATH, "(//table[contains(@class,'table')]//tbody/tr)[1]")
    NO_DATA_ROW = (By.XPATH, "//td[contains(@class,'dataTables_empty')]")

    INLINE_CREATED_AT = (By.XPATH, "//input[@placeholder='Filter by : Created At']")
    FILTER_PANEL_BTN = (By.ID, "filterToggleBtn")
    PANEL_DATE_RANGE = (By.ID, "date_range")

    APPLY_BTN = (By.XPATH, "//button[normalize-space()='Apply']")
    CLEAR_BTN = (By.XPATH, "//button[normalize-space()='Clear Filter']")
    FILTER_CLOSE_ICON = (By.CSS_SELECTOR, "div.offcanvas-header button.close")

    def goto_page(self):
        try:
            self.click(self.ENQUIRIES_MENU)
        except:
            pass

        self.driver.get("https://beta.digitathya.com/admin/enquires?reset_filters=1")
        self.wait_for_results()

    def wait_for_results(self):
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_elements(*self.FIRST_ROW) or d.find_elements(*self.NO_DATA_ROW)
        )

    def search(self, text):
        self.type(self.SEARCH_BOX, text)
        try:
            elem = self.driver.find_element(*self.SEARCH_BOX)
            elem.send_keys("\n")
        except:
            pass

    def open_inline_calendar(self):
        # open inline calendar
        self.click(self.INLINE_CREATED_AT)
        time.sleep(0.25)

    def open_filter_panel(self):
        self.click(self.FILTER_PANEL_BTN)
        time.sleep(0.4)

    def close_filter_panel(self):
        try:
            # If offcanvas not visible -> nothing to do
            if not self.driver.find_elements(By.CSS_SELECTOR, "div.offcanvas.show"):
                return True

            # If close icon present, click it
            if self.driver.find_elements(*self.FILTER_CLOSE_ICON):
                try:
                    self.click(self.FILTER_CLOSE_ICON)
                    return True
                except:
                    pass

            # fallback: send ESC event to close
            self.driver.execute_script(
                "document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));"
            )
            time.sleep(0.12)
            return True
        except:
            return True

    # ----------------- INLINE FILTER -----------------
    def filter_inline_created_at(self, start, end):
        """
        Use FlatpickrRangePicker to select an inline date range.
        Returns True if the calendar/range is disabled (meaning no results expected).
        """
        self.open_inline_calendar()
        picker = FlatpickrRangePicker(self.driver)

        # Defensive: attempt selection; select_range returns True on success, False if disabled/click failed
        try:
            ok = picker.select_range(start, end)
        except Exception:
            ok = False

        # If select_range returned False -> assume dates are disabled and no rows should be present
        if not ok:
            # leave calendar open so tests can assert disabled day nodes OR close explicitly
            return True

        # otherwise selection done — small pause for UI to update
        time.sleep(0.25)
        return False

    # ----------------- PANEL FILTER -----------------
    def filter_panel_created_at(self, start, end):
        """
        Open the offcanvas panel and set created-at range using FlatpickrRangePicker.
        Returns True if panel selection was NOT possible (range disabled) and caller should expect no results.
        """
        self.open_filter_panel()
        picker = FlatpickrRangePicker(self.driver)

        # Open the date control inside panel
        try:
            self.click(self.PANEL_DATE_RANGE)
            time.sleep(0.25)
        except:
            # if date_range control missing, close panel and treat as failure
            try:
                self.close_filter_panel()
            except:
                pass
            return True

        # Try selecting; select_range returns True on success, False if disabled or click failure
        try:
            ok = picker.select_range(start, end)
        except Exception:
            ok = False

        if not ok:
            # selection failed due to disabled days — close panel and return flag
            try:
                self.close_filter_panel()
            except:
                pass
            return True

        # Apply if present
        try:
            self.click(self.APPLY_BTN)
        except:
            pass

        # Close panel for clean state
        try:
            self.close_filter_panel()
        except:
            pass

        return False

    # ----------------- TABLE HELPERS -----------------
    def has_no_results(self):
        """
        True when 'No matching entries found' row is visible.
        """
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_elements(*self.NO_DATA_ROW) or d.find_elements(*self.FIRST_ROW)
            )
            return bool(self.driver.find_elements(*self.NO_DATA_ROW))
        except:
            return False

    def is_row_present(self):
        return bool(self.driver.find_elements(*self.FIRST_ROW))

    def has_disabled_future_dates(self):
        """
        Return True if disabled day elements exist. Open inline calendar briefly if not visible.
        """
        try:
            # Open inline calendar if not present
            if not self.driver.find_elements(By.CSS_SELECTOR, "div.flatpickr-calendar.open"):
                try:
                    self.open_inline_calendar()
                except:
                    pass

            # small wait for DOM update
            time.sleep(0.12)
            disabled = self.driver.find_elements(By.CSS_SELECTOR, "span.flatpickr-day.flatpickr-disabled")
            # Attempt to close inline calendar (click outside via ESC) to restore state
            try:
                self.driver.execute_script(
                    "document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));"
                )
            except:
                pass

            return len(disabled) > 0
        except:
            return False
