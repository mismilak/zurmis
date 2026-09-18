from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="list"),
    path("category/<fslug:slug>/", views.category_detail, name="category"),
    path("tag/<fslug:slug>/", views.tag_detail, name="tag"),
    path("<fslug:slug>/", views.post_detail, name="detail"),
]
