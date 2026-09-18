"""فیلترها و تگ‌های کمکی قالب."""
from django import template
from django.utils.safestring import mark_safe

from apps.core.jalali import to_jalali_string, to_persian_digits

register = template.Library()


@register.filter(name="jalali")
def jalali(value, fmt="long"):
    """تاریخ شمسی: {{ post.published_at|jalali }} یا {{ date|jalali:"numeric" }}"""
    return to_jalali_string(value, fmt)


@register.filter(name="fanum")
def fanum(value):
    """تبدیل ارقام انگلیسی به فارسی."""
    return to_persian_digits(value)


@register.filter(name="phone_link")
def phone_link(value):
    """تبدیل شماره تلفن فارسی/با فاصله به فرمت قابل استفاده در tel:"""
    if not value:
        return ""
    digits = str(value).translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
    return "".join(ch for ch in digits if ch.isdigit() or ch == "+")


ICONS = {
    "scale": "M12 3v18M5 7h14M7 7l-3 6a3 3 0 0 0 6 0L7 7Zm10 0-3 6a3 3 0 0 0 6 0l-3-6ZM8 21h8",
    "gavel": "m14 4 6 6M9 9l6 6M4.5 13.5 10 8m-5.5 5.5 2 2M3 21h8m2-13 2-2m4.5 8.5L21 11",
    "family": "M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm8 1a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM3 20a6 6 0 0 1 12 0M15.5 20a5 5 0 0 1 5.5-4.9",
    "home": "M3 10.5 12 3l9 7.5M5.5 9.5V20h13V9.5M10 20v-5h4v5",
    "briefcase": "M3 8h18v12H3V8Zm5 0V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18",
    "contract": "M7 3h7l5 5v13H7V3Zm7 0v5h5M9.5 13h6m-6 4h4",
    "shield": "M12 3 5 6v6c0 4.5 3 7.5 7 9 4-1.5 7-4.5 7-9V6l-7-3Zm-2.5 8.5 2 2 3.5-3.5",
    "bank": "M3 10h18M5 10v8m4-8v8m6-8v8m4-8v8M12 3l9 5H3l9-5ZM3 21h18",
    "doc": "M7 3h7l5 5v13H7V3Zm3 8h6m-6 4h6m-6-8h3",
    "check": "m5 13 4 4L19 7",
    "phone": "M4 5c0-1 1-2 2-2h2l2 5-2 1a12 12 0 0 0 5 5l1-2 5 2v2c0 1-1 2-2 2A16 16 0 0 1 4 5Z",
    "clock": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0-14v5l3 2",
    "star": "m12 4 2.4 4.9 5.4.8-3.9 3.8.9 5.4-4.8-2.5-4.8 2.5.9-5.4L4.2 9.7l5.4-.8L12 4Z",
    "users": "M8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm8 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM2 20a6 6 0 0 1 12 0m2-4.8A6 6 0 0 1 22 20",
    "message": "M4 5h16v11H9l-5 4V5Z",
    "video": "M3 6h12v12H3V6Zm12 4 6-3v10l-6-3",
    "book": "M4 5a2 2 0 0 1 2-2h12v18H6a2 2 0 0 1-2-2V5Zm2 13h12",
    "map": "M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Zm0-8.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z",
    "mail": "M3 6h18v12H3V6Zm0 1 9 7 9-7",
    "award": "M12 14a5 5 0 1 0 0-10 5 5 0 0 0 0 10Zm-3 .8L7 21l5-2.2L17 21l-2-6.2",
}


@register.simple_tag(name="icon")
def icon(name, css_class="icon"):
    """رندر آیکون SVG درون‌خطی."""
    path = ICONS.get(name, ICONS["check"])
    return mark_safe(
        f'<svg class="{css_class}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="{path}"/></svg>'
    )
