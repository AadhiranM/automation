import pytest

from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage
)

from pages.superadmin.Manufacturer.sa_manufacturer_filter_page import (
    SAManufacturerFilterPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerFilters:

    # =====================================================
    # INITIAL STATE
    # =====================================================

    def test_filter_initial_state(
            self,
            setup
    ):

        SAManufacturerListPage(
            setup
        ).goto_page()

        filter_page = (
            SAManufacturerFilterPage(
                setup
            )
        )

        filter_page.open_filter_panel()

        assert not (
            filter_page.is_apply_enabled()
        )

        assert not (
            filter_page.is_clear_enabled()
        )

    # =====================================================
    # COMPANY NAME
    # =====================================================

    def test_filter_by_company_name(
            self,
            setup
    ):

        SAManufacturerListPage(
            setup
        ).goto_page()

        filter_page = (
            SAManufacturerFilterPage(
                setup
            )
        )

        filter_page.filter_by_company_name(
            "TechNova"
        )

        assert (
            filter_page.is_row_present()
        )

    # =====================================================
    # EMAIL
    # =====================================================

    def test_filter_by_business_email(
            self,
            setup
    ):

        SAManufacturerListPage(
            setup
        ).goto_page()

        filter_page = (
            SAManufacturerFilterPage(
                setup
            )
        )

        filter_page.filter_by_business_email(
            "mailinator.com"
        )

        assert (
            filter_page.is_row_present()
        )

    # =====================================================
    # PAN
    # =====================================================

    def test_filter_by_pan_number(
            self,
            setup
    ):

        SAManufacturerListPage(
            setup
        ).goto_page()

        filter_page = (
            SAManufacturerFilterPage(
                setup
            )
        )

        filter_page.filter_by_pan_number(
            "ABCDE1234F"
        )

        assert (
            filter_page.is_row_present()
        )

    # =====================================================
    # STATUS
    # =====================================================

    def test_filter_by_approval_status(
            self,
            setup
    ):

        SAManufacturerListPage(
            setup
        ).goto_page()

        filter_page = (
            SAManufacturerFilterPage(
                setup
            )
        )

        filter_page.filter_by_approval_status()

        assert (
            filter_page.is_row_present()
        )

    # =====================================================
    # CLEAR FILTER
    # =====================================================

    def test_clear_filter(
            self,
            setup
    ):

        SAManufacturerListPage(
            setup
        ).goto_page()

        filter_page = (
            SAManufacturerFilterPage(
                setup
            )
        )

        filter_page.open_filter_panel()

        filter_page.type(
            filter_page.COMPANY_NAME,
            "TechNova"
        )

        filter_page.type(
            filter_page.BUSINESS_EMAIL,
            "mailinator.com"
        )

        filter_page.type(
            filter_page.PAN_NUMBER,
            "ABCDE1234F"
        )

        filter_page.click_clear()

        assert (
            filter_page.is_company_name_empty()
        )

        assert (
            filter_page.is_business_email_empty()
        )

        assert (
            filter_page.is_pan_number_empty()
        )