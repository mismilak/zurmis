from django.contrib import admin
from django.utils.html import format_html

from .models import Video, VideoCategory


@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "aparat_preview", "is_featured", "is_published", "order")
    list_editable = ("is_featured", "is_published", "order")
    list_filter = ("is_published", "is_featured", "category")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("مشخصات ویدیو", {
            "fields": ("title", "slug", "category", "aparat_url", "duration", "cover", "description"),
            "description": "کافی است لینک ویدیو در آپارات را وارد کنید؛ کد ویدیو به‌صورت خودکار استخراج می‌شود.",
        }),
        ("انتشار", {"fields": ("is_published", "is_featured", "published_at", "order")}),
    )

    @admin.display(description="لینک آپارات")
    def aparat_preview(self, obj):
        if not obj.watch_url:
            return "—"
        return format_html('<a href="{}" target="_blank" rel="noopener">مشاهده</a>', obj.watch_url)
