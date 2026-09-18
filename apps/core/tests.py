"""تست‌های دودکش‌ای (smoke tests) برای اطمینان از سلامت صفحات و فرم‌ها."""
from django.test import TestCase
from django.urls import reverse

from apps.blog.models import Category, Post
from apps.core.models import ConsultationRequest, PracticeArea, SiteSetting
from apps.videos.models import Video, extract_aparat_hash


class PagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        SiteSetting.load()
        cls.area = PracticeArea.objects.create(
            title="دعاوی حقوقی", short_description="توضیح کوتاه", order=1
        )
        category = Category.objects.create(name="عمومی")
        cls.post = Post.objects.create(
            title="نمونه مقاله حقوقی", category=category, content="<p>متن نمونه</p>", status="published"
        )
        cls.video = Video.objects.create(
            title="ویدیو نمونه", aparat_url="https://www.aparat.com/v/abcd1"
        )

    def test_home_page(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "درخواست مشاوره")

    def test_public_pages(self):
        for url in [
            reverse("blog:list"),
            reverse("videos:list"),
            reverse("core:faq"),
            reverse("core:contact"),
            self.area.get_absolute_url(),
            self.post.get_absolute_url(),
            self.video.get_absolute_url(),
            "/sitemap.xml",
            "/robots.txt",
        ]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_persian_slug_is_used(self):
        self.assertEqual(self.area.slug, "دعاوی-حقوقی")


class ConsultationFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        SiteSetting.load()

    def test_valid_request_is_saved(self):
        response = self.client.post(
            reverse("core:consultation_create"),
            {"full_name": "کاربر آزمایشی", "phone": "۰۹۱۲۱۲۳۴۵۶۷", "message": "متن پیام"},
            headers={"x-requested-with": "XMLHttpRequest"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        # ارقام فارسی به انگلیسی تبدیل می‌شوند
        self.assertEqual(ConsultationRequest.objects.get().phone, "09121234567")

    def test_invalid_phone_is_rejected(self):
        response = self.client.post(
            reverse("core:consultation_create"),
            {"full_name": "کاربر", "phone": "123", "message": "متن"},
            headers={"x-requested-with": "XMLHttpRequest"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.json()["errors"])

    def test_honeypot_blocks_bots(self):
        self.client.post(
            reverse("core:consultation_create"),
            {"full_name": "ربات", "phone": "09121234567", "message": "تبلیغ", "website": "http://spam"},
            headers={"x-requested-with": "XMLHttpRequest"},
        )
        self.assertEqual(ConsultationRequest.objects.count(), 0)


class AparatTests(TestCase):
    def test_hash_extraction(self):
        cases = {
            "https://www.aparat.com/v/xY12ab": "xY12ab",
            "https://aparat.com/v/xY12ab/": "xY12ab",
            "https://www.aparat.com/video/video/embed/videohash/xY12ab/vt/frame": "xY12ab",
            "xY12ab": "xY12ab",
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(extract_aparat_hash(value), expected)

    def test_embed_url(self):
        video = Video.objects.create(title="تست", aparat_url="https://www.aparat.com/v/xY12ab")
        self.assertIn("embed/videohash/xY12ab", video.embed_url)
