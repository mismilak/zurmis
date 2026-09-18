"""ویوهای بخش اصلی سایت."""
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.blog.models import Post
from apps.videos.models import Video

from .forms import ConsultationForm
from .models import FAQ, Credential, Page, PracticeArea, ProcessStep, SiteSetting, Stat, Testimonial


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def home(request):
    """صفحه نخست شامل تمام بخش‌های معرفی تا تماس."""
    context = {
        "practice_areas": PracticeArea.objects.filter(is_active=True, is_featured=True),
        "stats": Stat.objects.filter(is_active=True),
        "steps": ProcessStep.objects.filter(is_active=True),
        "educations": Credential.objects.filter(is_active=True, kind="education"),
        "experiences": Credential.objects.filter(is_active=True, kind="experience"),
        "certificates": Credential.objects.filter(
            is_active=True, kind__in=["certificate", "membership"]
        ),
        "testimonials": Testimonial.objects.filter(is_published=True)[:9],
        "faqs": FAQ.objects.filter(is_published=True)[:8],
        "posts": Post.published.select_related("category")[:3],
        "videos": Video.objects.filter(is_published=True, is_featured=True)[:6],
        "form": ConsultationForm(),
    }
    return render(request, "core/home.html", context)


def practice_detail(request, slug):
    area = get_object_or_404(PracticeArea, slug=slug, is_active=True)
    context = {
        "area": area,
        "others": PracticeArea.objects.filter(is_active=True).exclude(pk=area.pk)[:6],
        "posts": Post.published.filter(category__name__icontains=area.title)[:3],
        "form": ConsultationForm(initial={"subject": area}),
        "meta_title": f"{area.title} | وکالت و مشاوره تخصصی",
        "meta_description": area.short_description,
    }
    return render(request, "core/practice_detail.html", context)


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(
        request,
        "core/page_detail.html",
        {"page": page, "meta_title": page.title},
    )


def faq_list(request):
    return render(
        request,
        "core/faq.html",
        {"faqs": FAQ.objects.filter(is_published=True), "meta_title": "پرسش‌های متداول حقوقی"},
    )


def contact(request):
    return render(
        request,
        "core/contact.html",
        {"form": ConsultationForm(), "meta_title": "تماس با ما و درخواست مشاوره"},
    )


@require_POST
def consultation_create(request):
    """ثبت درخواست مشاوره از فرم سایت (پشتیبانی از ارسال معمولی و AJAX)."""
    form = ConsultationForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.ip_address = _client_ip(request)
        obj.save()
        _notify_new_request(obj)
        success_text = "درخواست شما با موفقیت ثبت شد. به‌زودی با شما تماس می‌گیریم."
        if _is_ajax(request):
            return JsonResponse({"ok": True, "message": success_text})
        messages.success(request, success_text)
        return redirect(request.POST.get("next") or "/#consultation")

    error_text = "لطفاً خطاهای فرم را برطرف کنید."
    if _is_ajax(request):
        return JsonResponse({"ok": False, "errors": form.errors, "message": error_text}, status=400)
    messages.error(request, error_text)
    return render(request, "core/contact.html", {"form": form}, status=400)


def _notify_new_request(obj):
    """ارسال ایمیل اطلاع‌رسانی در صورت تنظیم بودن SMTP."""
    target = getattr(settings, "NOTIFY_EMAIL", "")
    if not target:
        return
    body = (
        f"درخواست مشاوره جدید\n\n"
        f"نام: {obj.full_name}\n"
        f"تلفن: {obj.phone}\n"
        f"ایمیل: {obj.email or '-'}\n"
        f"موضوع: {obj.subject or '-'}\n"
        f"زمان مناسب تماس: {obj.preferred_time or '-'}\n\n"
        f"متن پیام:\n{obj.message}\n"
    )
    try:
        send_mail("درخواست مشاوره جدید از وب‌سایت", body, settings.DEFAULT_FROM_EMAIL, [target])
    except Exception:  # noqa: BLE001 - نبود ایمیل نباید ثبت درخواست را خراب کند
        pass


def search(request):
    """جست‌وجوی سراسری در مقالات، ویدیوها و خدمات."""
    query = (request.GET.get("q") or "").strip()
    posts = videos = areas = []
    if query:
        posts = Post.published.filter(title__icontains=query)[:10]
        videos = Video.objects.filter(is_published=True, title__icontains=query)[:10]
        areas = PracticeArea.objects.filter(is_active=True, title__icontains=query)[:10]
    return render(
        request,
        "core/search.html",
        {
            "query": query,
            "posts": posts,
            "videos": videos,
            "areas": areas,
            "meta_title": f"نتایج جست‌وجو برای «{query}»" if query else "جست‌وجو",
        },
    )


def robots_txt(request):
    site = SiteSetting.load()
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Allow: /",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def error_404(request, exception=None):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
