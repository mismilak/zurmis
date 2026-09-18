from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, register_converter

from apps.core.converters import UnicodeSlugConverter
from apps.core.sitemaps import SITEMAPS

# ثبت کانورتر اسلاگ فارسی پیش از بارگذاری urlpatterns اپ‌ها
register_converter(UnicodeSlugConverter, "fslug")
from apps.core.views import robots_txt

handler404 = "apps.core.views.error_404"
handler500 = "apps.core.views.error_500"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("blog/", include("apps.blog.urls")),
    path("videos/", include("apps.videos.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
