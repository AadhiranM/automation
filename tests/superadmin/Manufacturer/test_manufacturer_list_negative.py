import pytest
from datetime import date, timedelta

from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerListNegative:

    def test_filter_created_date_range_no_data(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()

        # Pick OLD past dates (safe no data)
        start = date.today() - timedelta(days=400)
        end = date.today() - timedelta(days=390)

        page.filter_inline_created_at(start, end)

        if page.has_no_data_message():
            assert page.get_no_data_message() == "No matching entries found"
        else:
            pytest.fail("Expected 'No matching entries found' message")
