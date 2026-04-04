import pytest
from datetime import date, timedelta
from pages.superadmin.QRManagement.sa_variant_list_page import SAVariantListPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestVariantListNegative:

    def test_filter_created_date_no_data(self, setup):
        page = SAVariantListPage(setup)
        page.goto_page()

        start = date.today() - timedelta(days=500)
        end = date.today() - timedelta(days=480)

        page.filter_inline_created_at(start, end)

        assert page.has_no_data_message()
        assert page.get_no_data_message() == "No matching entries found"