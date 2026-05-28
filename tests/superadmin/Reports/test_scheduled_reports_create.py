import pytest

from pages.superadmin.Reports.sa_scheduled_reports_list_page import (
    SAScheduledReportsPage
)

from pages.superadmin.Reports.sa_scheduled_reports_create_page import (
    SAScheduledReportsCreatePage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestScheduledReportsCreate:

    def test_create_scan_analytics_report(self, setup):
        list_page = SAScheduledReportsPage(setup)
        create_page = SAScheduledReportsCreatePage(setup)

        list_page.goto_page()
        list_page.click_create()

        create_page.create_schedule_report(
            report_name="Scan Analytics Report",
            file_format="CSV",
            mail_time="2",
            duration="Daily",
            manufacturer_required=True
        )

    def test_create_product_analysis_report(self, setup):
        list_page = SAScheduledReportsPage(setup)
        create_page = SAScheduledReportsCreatePage(setup)

        list_page.goto_page()
        list_page.click_create()

        create_page.create_schedule_report(
            report_name="Product Analysis Report",
            file_format="XLSX",
            mail_time="3",
            duration="Weekly",
            manufacturer_required=True
        )