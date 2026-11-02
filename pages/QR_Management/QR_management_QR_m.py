import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class QR_Management_QR_m_Page:
    ## Xpath for all the elements
    QR_Management= (By.XPATH, "//span[@class='nav-name'][normalize-space()='QR Management']")
    Qr_management = (By.XPATH, "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='QR Management']")
    request_QR_code = (By.XPATH, "//a[normalize-space()='Request QR Code']")
    import_btn=(By.XPATH,"//button[normalize-space()='Import']")
    import_continue=(By.XPATH,"//button[@id='continueToImportBtn']")
    upload_QR_file=(By.XPATH,"//input[@id='fileInput']")
    upload_btn=(By.XPATH,"//button[@id='uploadButton']")
    product_sku_id_opt = (By.XPATH, "//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Product SKU ID']")
    product_sku_field=(By.XPATH,"//div[@bp-field-name='product_ref_id']//input[@name='search_terms']")
    add_batch = (By.XPATH, "//input[@placeholder='Enter Batch Number']")
    variant_sku_id_opt = (By.XPATH, "//div[@bp-field-name='variant_sku_id']//div[@class='choices__inner']")
    variant_sku_field = (By.XPATH, "//div[@bp-field-name='variant_sku_id']//input[@name='search_terms']")
    Quantity=(By.XPATH, "//input[@placeholder='Enter Quantity']")
    Mftr_date = (By.XPATH, "//input[@id='manufacturing_date']")
    QR_image_format=(By.XPATH,"//div[@bp-field-name='qr_image_format']//div[@class='choices__inner']")
    product_name=(By.XPATH,"//input[@placeholder='Enter Product Name']")

    # Fixed calendar XPaths
    date_year = (By.XPATH, "//div[contains(@class,'flatpickr-calendar')]//input[@aria-label='Year']")
    date_month = (By.XPATH, "//div[contains(@class,'flatpickr-calendar')]//select[@aria-label='Month']")
    date_days = (By.XPATH, "//div[contains(@class,'flatpickr-calendar')]//span[contains(@class,'flatpickr-day')]")
    Exp_date = (By.XPATH, "//input[@id='expiry_date']")
    Dimension=(By.XPATH,"//div[@bp-field-name='image_size']//div[@class='choices__inner']")
    batch_delivery_location_opt = (By.XPATH, "//div[@bp-field-name='batch_location']//div[@class='choices__inner']")
    batch_delivery_location_field = (By.XPATH, "//div[@bp-field-name='batch_location']//input[@name='search_terms']")
    QR_Type_drpdwn=(By.XPATH,"//select[@id='serviceDropdown']")
    request_qr_code_btn = (By.XPATH, "//button[@type='submit']")


    ##filters
    search_value_field = (By.XPATH, "//input[@id='search-vale']")
    calender_icon = (By.XPATH, "//input[@id='datepicker-range']")
    drop_status=(By.XPATH, "//select[@id='idStatus']")
    table_first_batch_no=(By.XPATH, "//tbody/tr[1]/td[3]")
    start_date=(By.XPATH, "//tbody/tr[1]/td[8]")
    end_date=(By.XPATH, "//tbody/tr[1]/td[9]")
    actions_icon = (By.XPATH, "//i[@class='ri-more-fill align-middle']")
    view_icon= (By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-end qrmgnt-action-dropdown show']//a[@class='dropdown-item'][normalize-space()='View']")

    ##filter_toggle
    filter_toggle_btn = (By.XPATH, "//button[@id='filterToggleBtn']")
    product_name_field= (By.XPATH, "//input[@id='product_name']")
    table_first_product_name= (By.XPATH, "//tbody/tr[1]/td[2]")
    manufacturer_date_field= (By.XPATH, "//input[@id='manufacturing_date']")
    expiry_date_field= (By.XPATH, "//input[@id='expiry_date']")
    created_by_field= (By.XPATH, "//div[@class='choices__inner']")
    created_by_input_field= (By.XPATH, "//input[@placeholder='Search Created By']")
    apply_btn= (By.XPATH, "//button[normalize-space()='Apply']")


    ##import_logs
    import_logs_btn= (By.XPATH, "//a[normalize-space()='Import Logs']")
    import_logs_search_value_field= (By.XPATH, "//input[@id='search-vale']")
    import_logs_calender= (By.XPATH, "//input[@id='datepicker-range']")
    import_logs_status_drpdown= (By.XPATH, "//select[@id='idStatus']")
    import_logs_action_icon= (By.XPATH, "//tbody/tr[1]/td[8]//i[@class='ri-more-fill align-middle']")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---------------- Actions ----------------

    def Click_QR_management(self):
        self.driver.find_element(*self.QR_Management).click()

    def Click_Qr_management(self):
        self.driver.find_element(*self.Qr_management).click()

    def Click_import_btn(self):
        self.driver.find_element(*self.import_btn).click()

    def Click_import_continue_btn(self):
        self.driver.find_element(*self.import_continue).click()

    # def Click_upload_btn(self):
    #     self.driver.find_element(*self.upload_btn).click()

    def Click_upload_btn(self):
        upload_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.upload_btn)
        )
        upload_button.click()

    def Enter_upload_QR_file(self,upload_file):
        self.driver.find_element(*self.upload_QR_file).send_keys(upload_file)

    def Click_request_QR_button(self):
        self.driver.find_element(*self.request_QR_code).click()

    def click_product_skuID_opt(self):
        self.driver.find_element(*self.product_sku_id_opt).click()

    def Enter_product_sku_field(self,sku_id):
        ele=self.driver.find_element(*self.product_sku_field)
        ele.send_keys(sku_id)
        time.sleep(2)
        ele.send_keys(Keys.ENTER)

    def Enter_add_batch(self, batch_no):
        self.driver.find_element(*self.add_batch).send_keys(batch_no)

    def Click_product_name(self):
        self.driver.find_element(*self.product_name).click()

    # def Enter_Quantity(self, quantity):
    #     self.driver.find_element(*self.Quantity).send_keys(quantity)

    def Enter_Quantity(self, quantity):
        quantity_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.Quantity)
        )

        quantity_field.clear()
        quantity_field.send_keys(str(quantity))

    def is_popup_message_present(self, expected_text):
        try:
            # Get the entire visible page text
            body_text = self.driver.find_element(By.TAG_NAME, "body").text

            if expected_text.lower() in body_text.lower():
                return True
            else:
                return False

        except Exception:
            return False

    def is_variant_field_editable(self):
        try:
            element = self.driver.find_element(
                By.XPATH,
                "//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Variant SKU ID']"
            )

            # Check aria-disabled attribute
            aria_disabled = element.get_attribute("aria-disabled")

            print("aria-disabled:", aria_disabled)  # debug

            if aria_disabled == "true":
                return False
            else:
                return True

        except Exception as e:
            print("Error:", e)
            return False

    def Click_variant_skuID_opt(self):
        self.driver.find_element(*self.variant_sku_id_opt).click()

    def Enter_varinat_sku_field(self, variant_sku_field):
        variant=self.driver.find_element(*self.variant_sku_field)
        variant.send_keys(variant_sku_field)
        variant.send_keys(Keys.ENTER)

    def Click_manufacturer_date(self):
        self.driver.find_element(*self.Mftr_date).click()

    def Click_expiry_date(self):
        self.driver.find_element(*self.Exp_date).click()

    def select_date(self, date_string):
        day, month, year = date_string.split("-")
        month_name = calendar.month_name[int(month)]

        calendar_popup = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]"

        # YEAR
        year_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, calendar_popup + "//input[@aria-label='Year']")
            )
        )
        year_input.click()
        year_input.clear()
        year_input.send_keys(year)

        # MONTH
        month_dropdown = Select(
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, calendar_popup + "//select[@aria-label='Month']")
                )
            )
        )
        month_dropdown.select_by_visible_text(month_name)


        # DAY - select only from the requested month
        days = self.driver.find_elements(
            By.XPATH,
            calendar_popup + "//span[contains(@class,'flatpickr-day')]"
        )

        date_selected = False

        for d in days:
            classes = d.get_attribute("class")

            if (
                    d.text == str(int(day))
                    and "prevMonthDay" not in classes
                    and "nextMonthDay" not in classes
                    and "disabled" not in classes
            ):
                d.click()
                date_selected = True
                break

        if not date_selected:
            raise Exception(
                f"Date {date_string} was not found in the selected calendar month."
            )


    def set_manufacturing_date(self, date_string):
        self.wait.until(EC.element_to_be_clickable(self.Mftr_date)).click()
        self.select_date(date_string)

    def set_expiry_date(self, date_string):
        self.wait.until(EC.element_to_be_clickable(self.Exp_date)).click()
        self.select_date(date_string)

    def select_dimension(self, dimension):
        self.driver.find_element(*self.Dimension).click()
        time.sleep(1)
        dimension_xpath = (
            f"//div[@bp-field-name='image_size']"
            f"//div[contains(@class,'choices__list--dropdown')]"
            f"//div[normalize-space()='{dimension}']"
        )

        self.driver.find_element(By.XPATH, dimension_xpath).click()

    def select_QR_Type_drpdwn(self,QR_Type):
        drpdwn_qr_type = Select(self.driver.find_element(*self.QR_Type_drpdwn))
        drpdwn_qr_type.select_by_visible_text(QR_Type)

    def click_batch_delivery_opt(self):
        self.driver.find_element(*self.batch_delivery_location_opt).click()

    def Enter_batch_delivery_field(self,delivery_field_value):
        add=self.driver.find_element(*self.batch_delivery_location_field)
        add.clear()
        add.send_keys(delivery_field_value)
        time.sleep(2)
        add.send_keys(Keys.ENTER)

    def select_QR_Image_format(self,image_format):
        self.driver.find_element(*self.QR_image_format).click()
        time.sleep(1)
        image_format_xpath = f"//div[@bp-field-name='qr_image_format']//div[@role='listbox']//div[@role='listbox']//div[normalize-space()='{image_format}']"
        # image_format_xpath="//div[@bp-field-name='qr_image_format']//div[@class='choices__list choices__list--dropdown']//div[@id='choices--qrImageFormatDropdown-item-choice-2']"
        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, image_format_xpath))
        )
        option.click()
    def click_request_QR_code_button(self):
        btn=self.driver.find_element(*self.request_qr_code_btn)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        self.driver.execute_script("arguments[0].click();", btn)



    ##filters_path

    def Enter_search_value(self, search_value):
        search_field = self.driver.find_element(*self.search_value_field)
        search_field.clear()
        search_field.send_keys(search_value)
        time.sleep(2)

    def Click_calender_icon(self):
        self.driver.find_element(*self.calender_icon).click()

    def Enter_select_status(self, status_value):
        drp = Select(self.driver.find_element(*self.drop_status))
        drp.select_by_visible_text(status_value)

    def Click_actions_icon(self):
        actions_icon = self.wait.until(
            EC.visibility_of_element_located(self.actions_icon)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            actions_icon
        )

        self.wait.until(
            EC.element_to_be_clickable(self.actions_icon)
        ).click()

    def Click_view_icon(self):
        view_icon = self.wait.until(
            EC.visibility_of_element_located(self.view_icon)
        )

        self.wait.until(
            EC.element_to_be_clickable(self.view_icon)
        ).click()

    def select_date_range(self, start_date, end_date):
        """
        Flatpickr range selection
        start_date / end_date → YYYY-MM-DD
        """

        start_year, start_month, start_day = start_date.split("-")
        end_year, end_month, end_day = end_date.split("-")

        start_month_name = calendar.month_name[int(start_month)]
        end_month_name = calendar.month_name[int(end_month)]

        calendar_popup = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]"

        self.wait.until(EC.visibility_of_element_located((By.XPATH, calendar_popup)))

        # START DATE
        year_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, calendar_popup + "//input[@aria-label='Year']"))
        )
        year_input.clear()
        year_input.send_keys(start_year)

        month_dropdown = Select(
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, calendar_popup + "//select[@aria-label='Month']"))
            )
        )
        month_dropdown.select_by_visible_text(start_month_name)
        time.sleep(0.5)

        for d in self.driver.find_elements(By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"):
            classes = d.get_attribute("class")
            if (
                    d.text == str(int(start_day))
                    and "flatpickr-disabled" not in classes
                    and "notAllowed" not in classes
                    and "prevMonthDay" not in classes
                    and "nextMonthDay" not in classes
            ):
                d.click()
                break
        time.sleep(1)

        # END DATE
        if start_year != end_year or start_month_name != end_month_name:
            year_input.clear()
            year_input.send_keys(end_year)
            month_dropdown.select_by_visible_text(end_month_name)
            time.sleep(1)

        for d in self.driver.find_elements(By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"):

            classes = d.get_attribute("class")

            if (
                    d.text == str(int(end_day))
                    and "flatpickr-disabled" not in classes
                    and "notAllowed" not in classes
                    and "prevMonthDay" not in classes
                    and "nextMonthDay" not in classes
            ):
                d.click()
                break

    def Click_filter_toggle_btn(self):
        self.driver.find_element(*self.filter_toggle_btn).click()

    def Enter_product_name(self, product_name):
        product_name_field = self.driver.find_element(*self.product_name_field)
        product_name_field.clear()
        product_name_field.send_keys(product_name)

    def Click_manufacturer_date_field(self):
        self.driver.find_element(*self.manufacturer_date_field).click()

    def Click_expiry_date_field(self):
        self.driver.find_element(*self.expiry_date_field).click()

    def Click_created_by_field(self):
        self.driver.find_element(*self.created_by_field).click()

    def Enter_created_by_input_field(self, created_by_value):
        created_by_input_field = self.driver.find_element(*self.created_by_input_field)
        created_by_input_field.clear()
        created_by_input_field.send_keys(created_by_value)

    def Click_apply_btn(self):
        self.driver.find_element(*self.apply_btn).click()

    def filter_toggle_manufacturing_date(self, date_string):
        self.wait.until(EC.element_to_be_clickable(self.manufacturer_date_field)).click()
        time.sleep(1)
        self.select_date(date_string)

    def filter_toggle_expiry_date(self, date_string):
        self.wait.until(EC.element_to_be_clickable(self.expiry_date_field)).click()
        time.sleep(1)
        self.select_date(date_string)

     ###import_logs

    def Click_import_logs_btn(self):
        self.wait.until(
            EC.element_to_be_clickable(self.import_logs_btn)
        ).click()

    def Enter_import_logs_search_value_field(self, search_value):
        search_field = self.wait.until(
            EC.visibility_of_element_located(
                self.import_logs_search_value_field
            )
        )
        search_field.clear()
        search_field.send_keys(search_value)

    def Click_import_logs_calender(self):
        self.wait.until(
            EC.element_to_be_clickable(self.import_logs_calender)
        ).click()

    def Select_import_logs_status_drpdown(self, status):
        status_dropdown = self.wait.until(
            EC.visibility_of_element_located(
                self.import_logs_status_drpdown
            )
        )
        Select(status_dropdown).select_by_visible_text(status)

    def Click_import_logs_action_icon(self):
        self.wait.until(
            EC.element_to_be_clickable(self.import_logs_action_icon)
        ).click()

