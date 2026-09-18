from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Category, Post
from apps.videos.models import Video

from .models import Page, PracticeArea


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return ["core:home", "core:contact", "core:faq", "blog:list", "videos:list"]

    def location(self, item):
        return reverse(item)


class PracticeSitemap(Sitemap):
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return PracticeArea.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class PostSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Category.objects.all()


class VideoSitemap(Sitemap):
    priority = 0.7

    def items(self):
        return Video.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class PageSitemap(Sitemap):
    priority = 0.4

    def items(self):
        return Page.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


SITEMAPS = {
    "static": StaticSitemap,
    "services": PracticeSitemap,
    "posts": PostSitemap,
    "categories": CategorySitemap,
    "videos": VideoSitemap,
    "pages": PageSitemap,
}
