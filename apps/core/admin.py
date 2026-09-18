"""پنل مدیریت بخش اصلی سایت."""
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    FAQ,
    ConsultationRequest,
    Credential,
    Page,
    PracticeArea,
    ProcessStep,
    SiteSetting,
    Stat,
    Testimonial,
)

admin.site.site_header = "پنل مدیریت وب‌سایت وکالت"
admin.site.site_title = "مدیریت سایت"
admin.site.index_title = "مدیریت محتوای سایت"


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("اطلاعات وکیل", {
            "fields": ("site_name", "lawyer_name", "job_title", "bar_association", "license_number",
                       "profile_image", "logo", "favicon"),
        }),
        ("صفحه نخست", {"fields": ("hero_title", "hero_subtitle", "hero_image")}),
        ("معرفی", {"fields": ("about_short", "about_full")}),
        ("راه‌های ارتباطی", {
            "fields": ("phone", "phone_secondary", "mobile", "whatsapp", "telegram", "eitaa",
                       "instagram", "aparat_channel", "linkedin", "email"),
        }),
        ("دفتر", {"fields": ("address", "working_hours", "map_embed")}),
        ("سئو و ابزارها", {
            "fields": ("meta_description", "meta_keywords", "enamad_code", "analytics_code",
                       "footer_note", "consultation_note"),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PracticeArea)
class PracticeAreaAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "is_featured", "is_active", "order")
    list_editable = ("is_featured", "is_active", "order")
    list_filter = ("is_featured", "is_active")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "organization", "period", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("kind", "is_active")
    search_fields = ("title", "organization")


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "suffix", "is_active", "order")
    list_editable = ("value", "suffix", "is_active", "order")


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "rating", "is_published", "order")
    list_editable = ("is_published", "order")
    list_filter = ("is_published", "rating")
    search_fields = ("name", "content")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_published", "order")
    list_editable = ("is_published", "order")
    search_fields = ("question", "answer")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "show_in_footer")
    list_editable = ("is_published", "show_in_footer")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_link", "subject", "status", "created_at")
    list_filter = ("status", "subject", "created_at")
    search_fields = ("full_name", "phone", "email", "message")
    readonly_fields = ("full_name", "phone", "email", "subject", "preferred_time", "message",
                       "ip_address", "created_at")
    fields = readonly_fields + ("status", "admin_note")
    date_hierarchy = "created_at"
    actions = ["mark_in_progress", "mark_done", "mark_archived"]

    @admin.display(description="شماره تماس")
    def phone_link(self, obj):
        return format_html('<a href="tel:{}" dir="ltr">{}</a>', obj.phone, obj.phone)

    def has_add_permission(self, request):
        return False

    @admin.action(description="علامت‌گذاری به عنوان «در حال پیگیری»")
    def mark_in_progress(self, request, queryset):
        queryset.update(status="in_progress")

    @admin.action(description="علامت‌گذاری به عنوان «انجام شد»")
    def mark_done(self, request, queryset):
        queryset.update(status="done")

    @admin.action(description="بایگانی کردن")
    def mark_archived(self, request, queryset):
        queryset.update(status="archived")
