import pytest
from datetime import date, timedelta
from pages.superadmin.QRManagement.sa_product_list_page import SAProductListPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestProductListNegative:

    def test_search_no_result(self, setup):
        page = SAProductListPage(setup)
        page.goto_page()
        page.search("INVALID_PRODUCT_123")

        assert page.has_no_data()
