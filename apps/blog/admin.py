from django.contrib import admin

from .models import Category, Comment, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("name", "content", "is_approved", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "is_featured", "published_at", "views")
    list_editable = ("status", "is_featured")
    list_filter = ("status", "is_featured", "category", "published_at")
    search_fields = ("title", "content", "summary")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "published_at"
    inlines = [CommentInline]
    fieldsets = (
        ("محتوای اصلی", {"fields": ("title", "slug", "category", "tags", "cover", "summary", "content")}),
        ("انتشار", {"fields": ("status", "published_at", "is_featured", "author_name")}),
        ("سئو", {"fields": ("meta_description",)}),
    )
    actions = ["publish_posts", "unpublish_posts"]

    @admin.action(description="انتشار مقالات انتخاب‌شده")
    def publish_posts(self, request, queryset):
        queryset.update(status="published")

    @admin.action(description="تبدیل به پیش‌نویس")
    def unpublish_posts(self, request, queryset):
        queryset.update(status="draft")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "is_approved", "created_at")
    list_editable = ("is_approved",)
    list_filter = ("is_approved", "created_at")
    search_fields = ("name", "content")
    actions = ["approve_comments"]

    @admin.action(description="تایید دیدگاه‌های انتخاب‌شده")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
