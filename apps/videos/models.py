"""مدل ویدیوهای آپارات."""
import re

from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.core.models import TimeStampedModel, fa_slugify

APARAT_HASH_RE = re.compile(r"(?:aparat\.com/)(?:v/|video/video/embed/videohash/)?([A-Za-z0-9]{6,})")


def extract_aparat_hash(value: str) -> str:
    """استخراج کد ویدیو از لینک آپارات؛ اگر خود کد وارد شود همان برگردانده می‌شود."""
    value = (value or "").strip()
    if not value:
        return ""
    match = APARAT_HASH_RE.search(value)
    if match:
        return match.group(1)
    if "/" not in value and " " not in value:
        return value
    return ""


class VideoCategory(models.Model):
    name = models.CharField("نام دسته", max_length=100, unique=True)
    slug = models.SlugField("نشانی اینترنتی", max_length=120, unique=True, allow_unicode=True, blank=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "دسته‌بندی ویدیو"
        verbose_name_plural = "دسته‌بندی ویدیوها"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = fa_slugify(self.name)
        super().save(*args, **kwargs)


class Video(TimeStampedModel):
    title = models.CharField("عنوان ویدیو", max_length=200)
    slug = models.SlugField("نشانی اینترنتی", max_length=220, unique=True, allow_unicode=True, blank=True)
    category = models.ForeignKey(
        VideoCategory,
        verbose_name="دسته‌بندی",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="videos",
    )
    aparat_url = models.CharField(
        "لینک ویدیو در آپارات",
        max_length=300,
        help_text="لینک کامل ویدیو (مثال: https://www.aparat.com/v/abc123) یا فقط کد ویدیو",
    )
    aparat_hash = models.CharField("کد ویدیو", max_length=60, blank=True, editable=False)
    description = models.TextField("توضیحات", blank=True)
    cover = models.ImageField("تصویر بندانگشتی", upload_to="videos/", blank=True)
    duration = models.CharField("مدت زمان", max_length=20, blank=True, help_text="مثال: ۰۵:۳۲")
    is_featured = models.BooleanField("نمایش در صفحه نخست", default=True)
    is_published = models.BooleanField("منتشر شود", default=True)
    published_at = models.DateTimeField("تاریخ انتشار", default=timezone.now)
    views = models.PositiveIntegerField("تعداد بازدید", default=0, editable=False)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "ویدیو"
        verbose_name_plural = "ویدیوها"
        ordering = ["order", "-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = fa_slugify(self.title)
        self.aparat_hash = extract_aparat_hash(self.aparat_url)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("videos:detail", args=[self.slug])

    @property
    def embed_url(self):
        if not self.aparat_hash:
            return ""
        return f"https://www.aparat.com/video/video/embed/videohash/{self.aparat_hash}/vt/frame"

    @property
    def watch_url(self):
        if self.aparat_url.startswith("http"):
            return self.aparat_url
        return f"https://www.aparat.com/v/{self.aparat_hash}" if self.aparat_hash else ""

    @property
    def cover_url(self):
        if self.cover:
            return self.cover.url
        if self.aparat_hash:
            return f"https://www.aparat.com/video/video/thumbnail/videohash/{self.aparat_hash}"
        return ""
