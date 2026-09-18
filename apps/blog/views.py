"""ویوهای بخش مقالات."""
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Category, Post, Tag


def _paginate(request, queryset, per_page=9):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get("page"))


def _sidebar_context():
    return {
        "categories": Category.objects.annotate(
            posts_count=Count("posts", filter=Q(posts__status="published"))
        ),
        "popular_posts": Post.published.order_by("-views")[:5],
        "tags": Tag.objects.all()[:20],
    }


def post_list(request):
    query = (request.GET.get("q") or "").strip()
    posts = Post.published.select_related("category")
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    context = {
        "page_obj": _paginate(request, posts),
        "query": query,
        "featured": Post.published.filter(is_featured=True)[:3] if not query else [],
        "meta_title": "مقالات و اخبار حقوقی",
        "meta_description": "جدیدترین مقالات و نکات حقوقی؛ راهنمای گام‌به‌گام پرونده‌های حقوقی، کیفری، خانواده و ملکی.",
        **_sidebar_context(),
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.published.select_related("category").prefetch_related("tags"), slug=slug
    )
    Post.objects.filter(pk=post.pk).update(views=post.views + 1)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "دیدگاه شما ثبت شد و پس از تایید نمایش داده می‌شود.")
            return redirect(post.get_absolute_url() + "#comments")
        messages.error(request, "لطفاً فیلدهای دیدگاه را بررسی کنید.")
    else:
        form = CommentForm()

    related = (
        Post.published.filter(category=post.category).exclude(pk=post.pk)[:3]
        if post.category
        else Post.published.exclude(pk=post.pk)[:3]
    )
    context = {
        "post": post,
        "related": related,
        "form": form,
        "comments": post.approved_comments.prefetch_related("replies"),
        "meta_title": post.title,
        "meta_description": post.meta_description or post.summary[:160],
        **_sidebar_context(),
    }
    return render(request, "blog/post_detail.html", context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category)
    context = {
        "category": category,
        "page_obj": _paginate(request, posts),
        "meta_title": f"مقالات دسته «{category.name}»",
        "meta_description": category.description,
        **_sidebar_context(),
    }
    return render(request, "blog/post_list.html", context)


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.published.filter(tags=tag)
    context = {
        "tag": tag,
        "page_obj": _paginate(request, posts),
        "meta_title": f"مقالات با برچسب «{tag.name}»",
        **_sidebar_context(),
    }
    return render(request, "blog/post_list.html", context)
