"""ویوهای بخش ویدیوهای آپارات."""
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Video, VideoCategory


def video_list(request):
    videos = Video.objects.filter(is_published=True).select_related("category")
    category_slug = request.GET.get("category")
    active_category = None
    if category_slug:
        active_category = get_object_or_404(VideoCategory, slug=category_slug)
        videos = videos.filter(category=active_category)
    paginator = Paginator(videos, 12)
    context = {
        "page_obj": paginator.get_page(request.GET.get("page")),
        "categories": VideoCategory.objects.all(),
        "active_category": active_category,
        "meta_title": "ویدیوهای آموزشی حقوقی",
        "meta_description": "ویدیوهای آموزشی و نکات حقوقی؛ پاسخ به پرسش‌های پرتکرار به‌زبان ساده.",
    }
    return render(request, "videos/video_list.html", context)


def video_detail(request, slug):
    video = get_object_or_404(Video, slug=slug, is_published=True)
    Video.objects.filter(pk=video.pk).update(views=video.views + 1)
    context = {
        "video": video,
        "related": Video.objects.filter(is_published=True).exclude(pk=video.pk)[:6],
        "meta_title": video.title,
        "meta_description": video.description[:160],
    }
    return render(request, "videos/video_detail.html", context)
