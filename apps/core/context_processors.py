"""اطلاعات مشترک همه صفحات."""
from .models import Page, PracticeArea, SiteSetting


def site_settings(request):
    return {
        "site": SiteSetting.load(),
        "nav_practice_areas": PracticeArea.objects.filter(is_active=True)[:8],
        "footer_pages": Page.objects.filter(is_published=True, show_in_footer=True),
    }
