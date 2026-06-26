from pages.common.base_page import BasePage


class SAEnquiryViewPage(BasePage):

    def is_view_page_opened(self, enquiry_id):

        current_url = self.driver.current_url.lower()

        return (
            f"/{enquiry_id}/show" in current_url
        )