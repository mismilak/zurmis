"""مدل‌های بخش مقالات و اخبار حقوقی."""
import re

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

from apps.core.models import TimeStampedModel, fa_slugify


class Category(models.Model):
    name = models.CharField("نام دسته", max_length=100, unique=True)
    slug = models.SlugField("نشانی اینترنتی", max_length=120, unique=True, allow_unicode=True, blank=True)
    description = models.CharField("توضیح کوتاه", max_length=250, blank=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "دسته‌بندی مقالات"
        verbose_name_plural = "دسته‌بندی مقالات"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = fa_slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category", args=[self.slug])


class Tag(models.Model):
    name = models.CharField("نام برچسب", max_length=60, unique=True)
    slug = models.SlugField("نشانی اینترنتی", max_length=80, unique=True, allow_unicode=True, blank=True)

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = fa_slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:tag", args=[self.slug])


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(status="published", published_at__lte=timezone.now())
        )


class Post(TimeStampedModel):
    STATUS_CHOICES = [("draft", "پیش‌نویس"), ("published", "منتشر شده")]

    title = models.CharField("عنوان مقاله", max_length=200)
    slug = models.SlugField("نشانی اینترنتی", max_length=220, unique=True, allow_unicode=True, blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name="دسته‌بندی",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    tags = models.ManyToManyField(Tag, verbose_name="برچسب‌ها", blank=True, related_name="posts")
    summary = models.TextField("خلاصه مقاله", max_length=400, blank=True)
    content = models.TextField("متن مقاله (HTML مجاز است)")
    cover = models.ImageField("تصویر شاخص", upload_to="blog/", blank=True)
    author_name = models.CharField("نویسنده", max_length=120, blank=True)
    status = models.CharField("وضعیت", max_length=20, choices=STATUS_CHOICES, default="published")
    published_at = models.DateTimeField("تاریخ انتشار", default=timezone.now)
    is_featured = models.BooleanField("مقاله ویژه", default=False)
    views = models.PositiveIntegerField("تعداد بازدید", default=0, editable=False)
    meta_description = models.CharField("توضیحات متا (سئو)", max_length=300, blank=True)

    objects = models.Manager()
    published = PublishedPostManager()

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ["-published_at"]
        indexes = [models.Index(fields=["-published_at"]), models.Index(fields=["status"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = fa_slugify(self.title)
        if not self.summary:
            self.summary = strip_tags(self.content)[:300]
        if not self.meta_description:
            self.meta_description = strip_tags(self.summary)[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.slug])

    @property
    def reading_time(self):
        """زمان تقریبی مطالعه بر حسب دقیقه."""
        words = len(re.findall(r"\S+", strip_tags(self.content)))
        return max(1, round(words / 200))

    @property
    def approved_comments(self):
        return self.comments.filter(is_approved=True, parent__isnull=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name="مقاله", on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self",
        verbose_name="پاسخ به",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )
    name = models.CharField("نام", max_length=80)
    email = models.EmailField("ایمیل", blank=True)
    content = models.TextField("متن دیدگاه")
    is_approved = models.BooleanField("تایید شده", default=False)
    created_at = models.DateTimeField("تاریخ ثبت", default=timezone.now, editable=False)

    class Meta:
        verbose_name = "دیدگاه"
        verbose_name_plural = "دیدگاه‌ها"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.name} روی {self.post}"
