"""مدل‌های اصلی سایت: تنظیمات، خدمات، سوابق، نظرات، سوالات متداول و درخواست مشاوره."""
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def fa_slugify(value):
    """ساخت اسلاگ سازگار با فارسی (حروف فارسی حفظ می‌شوند)."""
    return slugify(value, allow_unicode=True) or "item"


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("تاریخ ایجاد", default=timezone.now, editable=False)
    updated_at = models.DateTimeField("آخرین ویرایش", auto_now=True)

    class Meta:
        abstract = True


class SiteSetting(models.Model):
    """تنظیمات کلی سایت (تک‌رکوردی)."""

    site_name = models.CharField("نام سایت", max_length=120, default="دفتر وکالت")
    lawyer_name = models.CharField("نام و نام خانوادگی وکیل", max_length=120, default="نام وکیل")
    job_title = models.CharField(
        "عنوان شغلی", max_length=160, default="وکیل پایه یک دادگستری و مشاور حقوقی"
    )
    bar_association = models.CharField(
        "کانون وکلای دادگستری", max_length=120, default="کانون وکلای دادگستری مرکز", blank=True
    )
    license_number = models.CharField("شماره پروانه وکالت", max_length=60, blank=True)
    hero_title = models.CharField(
        "تیتر اصلی صفحه نخست", max_length=200, default="دفاع حرفه‌ای از حقوق شما"
    )
    hero_subtitle = models.TextField(
        "توضیح کوتاه صفحه نخست",
        blank=True,
        default="مشاوره تخصصی و وکالت در پرونده‌های حقوقی، کیفری، خانواده و ملکی.",
    )
    hero_image = models.ImageField("تصویر صفحه نخست", upload_to="site/", blank=True)
    profile_image = models.ImageField("عکس پرسنلی وکیل", upload_to="site/", blank=True)
    logo = models.ImageField("لوگو", upload_to="site/", blank=True)
    favicon = models.ImageField("فاوآیکون", upload_to="site/", blank=True)

    about_short = models.TextField("معرفی کوتاه", blank=True)
    about_full = models.TextField("معرفی کامل (HTML مجاز است)", blank=True)

    phone = models.CharField("تلفن تماس", max_length=30, blank=True)
    phone_secondary = models.CharField("تلفن دوم", max_length=30, blank=True)
    mobile = models.CharField("موبایل", max_length=30, blank=True)
    whatsapp = models.CharField("واتساپ (با کد کشور، مثال: 989121234567)", max_length=30, blank=True)
    telegram = models.CharField("تلگرام (بدون @)", max_length=60, blank=True)
    eitaa = models.CharField("ایتا (بدون @)", max_length=60, blank=True)
    instagram = models.CharField("اینستاگرام (بدون @)", max_length=60, blank=True)
    aparat_channel = models.CharField("نام کانال آپارات (بدون @)", max_length=60, blank=True)
    linkedin = models.URLField("لینکدین", blank=True)
    email = models.EmailField("ایمیل", blank=True)

    address = models.TextField("آدرس دفتر", blank=True)
    working_hours = models.CharField(
        "ساعات کاری", max_length=160, blank=True, default="شنبه تا چهارشنبه، ۹ تا ۱۸"
    )
    map_embed = models.TextField(
        "کد امبد نقشه (iframe نشان یا گوگل‌مپ)",
        blank=True,
        help_text="کد iframe نقشه را اینجا قرار دهید.",
    )

    meta_description = models.CharField("توضیحات متا (سئو)", max_length=300, blank=True)
    meta_keywords = models.CharField("کلمات کلیدی (سئو)", max_length=300, blank=True)
    enamad_code = models.TextField("کد نماد اعتماد الکترونیکی", blank=True)
    analytics_code = models.TextField("کد آنالیتیکس / آمارگیر", blank=True)
    footer_note = models.CharField("متن فوتر", max_length=250, blank=True)
    consultation_note = models.CharField(
        "متن راهنمای فرم مشاوره",
        max_length=250,
        blank=True,
        default="درخواست شما در اسرع وقت بررسی و با شما تماس گرفته می‌شود.",
    )

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1  # تک‌رکوردی
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):  # جلوگیری از حذف رکورد تنظیمات
        raise ValidationError("امکان حذف تنظیمات سایت وجود ندارد.")

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def whatsapp_link(self):
        return f"https://wa.me/{self.whatsapp}" if self.whatsapp else ""

    @property
    def telegram_link(self):
        return f"https://t.me/{self.telegram}" if self.telegram else ""

    @property
    def eitaa_link(self):
        return f"https://eitaa.com/{self.eitaa}" if self.eitaa else ""

    @property
    def instagram_link(self):
        return f"https://instagram.com/{self.instagram}" if self.instagram else ""

    @property
    def aparat_link(self):
        return f"https://www.aparat.com/{self.aparat_channel}" if self.aparat_channel else ""


class PracticeArea(TimeStampedModel):
    """زمینه‌های تخصصی / خدمات حقوقی."""

    title = models.CharField("عنوان خدمت", max_length=120)
    slug = models.SlugField("نشانی اینترنتی", max_length=140, unique=True, allow_unicode=True, blank=True)
    icon = models.CharField(
        "آیکون",
        max_length=40,
        default="scale",
        help_text="یکی از: scale, gavel, family, home, briefcase, contract, shield, bank, doc, check",
    )
    short_description = models.CharField("توضیح کوتاه", max_length=250)
    description = models.TextField("توضیح کامل (HTML مجاز است)", blank=True)
    image = models.ImageField("تصویر", upload_to="practice/", blank=True)
    is_featured = models.BooleanField("نمایش در صفحه نخست", default=True)
    is_active = models.BooleanField("فعال", default=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "زمینه تخصصی / خدمت"
        verbose_name_plural = "زمینه‌های تخصصی و خدمات"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = fa_slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:practice_detail", args=[self.slug])


class Credential(models.Model):
    """سوابق تحصیلی، شغلی و افتخارات."""

    KIND_CHOICES = [
        ("education", "تحصیلات"),
        ("experience", "سوابق شغلی"),
        ("certificate", "گواهی‌نامه و افتخارات"),
        ("membership", "عضویت‌ها"),
    ]

    kind = models.CharField("نوع", max_length=20, choices=KIND_CHOICES, default="experience")
    title = models.CharField("عنوان", max_length=160)
    organization = models.CharField("سازمان / دانشگاه", max_length=160, blank=True)
    period = models.CharField("بازه زمانی", max_length=60, blank=True, help_text="مثال: ۱۳۹۵ تا ۱۴۰۰")
    description = models.TextField("توضیحات", blank=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "سابقه / افتخار"
        verbose_name_plural = "سوابق و افتخارات"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Stat(models.Model):
    """آمار و دستاوردها (تعداد پرونده، سال سابقه و ...)."""

    label = models.CharField("عنوان", max_length=80)
    value = models.PositiveIntegerField("عدد", default=0)
    suffix = models.CharField("پسوند", max_length=20, blank=True, help_text="مثال: + یا سال")
    icon = models.CharField("آیکون", max_length=40, default="check", blank=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "آمار"
        verbose_name_plural = "آمار و دستاوردها"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.label}: {self.value}"


class ProcessStep(models.Model):
    """مراحل همکاری با دفتر."""

    title = models.CharField("عنوان مرحله", max_length=120)
    description = models.TextField("توضیح", blank=True)
    icon = models.CharField("آیکون", max_length=40, default="check", blank=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "مرحله همکاری"
        verbose_name_plural = "مراحل همکاری"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Testimonial(TimeStampedModel):
    """نظرات موکلان."""

    name = models.CharField("نام موکل", max_length=80)
    role = models.CharField("عنوان / نوع پرونده", max_length=120, blank=True)
    content = models.TextField("متن نظر")
    avatar = models.ImageField("تصویر", upload_to="testimonials/", blank=True)
    rating = models.PositiveSmallIntegerField("امتیاز (۱ تا ۵)", default=5)
    is_published = models.BooleanField("منتشر شود", default=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "نظر موکل"
        verbose_name_plural = "نظرات موکلان"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.name

    @property
    def stars(self):
        return range(self.rating)


class FAQ(models.Model):
    """سوالات متداول."""

    question = models.CharField("پرسش", max_length=250)
    answer = models.TextField("پاسخ")
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)
    is_published = models.BooleanField("منتشر شود", default=True)

    class Meta:
        verbose_name = "پرسش متداول"
        verbose_name_plural = "پرسش‌های متداول"
        ordering = ["order", "id"]

    def __str__(self):
        return self.question


class Page(TimeStampedModel):
    """صفحات ثابت مثل قوانین و حریم خصوصی."""

    title = models.CharField("عنوان صفحه", max_length=160)
    slug = models.SlugField("نشانی اینترنتی", max_length=180, unique=True, allow_unicode=True, blank=True)
    content = models.TextField("محتوا (HTML مجاز است)")
    is_published = models.BooleanField("منتشر شود", default=True)
    show_in_footer = models.BooleanField("نمایش در فوتر", default=True)

    class Meta:
        verbose_name = "صفحه ثابت"
        verbose_name_plural = "صفحات ثابت"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = fa_slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:page_detail", args=[self.slug])


class ConsultationRequest(models.Model):
    """درخواست مشاوره ثبت‌شده از فرم سایت."""

    STATUS_CHOICES = [
        ("new", "جدید"),
        ("in_progress", "در حال پیگیری"),
        ("done", "انجام شد"),
        ("archived", "بایگانی"),
    ]

    full_name = models.CharField("نام و نام خانوادگی", max_length=120)
    phone = models.CharField("شماره تماس", max_length=20)
    email = models.EmailField("ایمیل", blank=True)
    subject = models.ForeignKey(
        PracticeArea,
        verbose_name="موضوع پرونده",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requests",
    )
    preferred_time = models.CharField("زمان مناسب تماس", max_length=120, blank=True)
    message = models.TextField("شرح مختصر موضوع")
    status = models.CharField("وضعیت", max_length=20, choices=STATUS_CHOICES, default="new")
    admin_note = models.TextField("یادداشت داخلی", blank=True)
    ip_address = models.GenericIPAddressField("آی‌پی", null=True, blank=True)
    created_at = models.DateTimeField("تاریخ ثبت", default=timezone.now, editable=False)

    class Meta:
        verbose_name = "درخواست مشاوره"
        verbose_name_plural = "درخواست‌های مشاوره"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.phone}"
