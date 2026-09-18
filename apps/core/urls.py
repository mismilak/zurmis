from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("consultation/", views.consultation_create, name="consultation_create"),
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq_list, name="faq"),
    path("search/", views.search, name="search"),
    path("services/<fslug:slug>/", views.practice_detail, name="practice_detail"),
    path("page/<fslug:slug>/", views.page_detail, name="page_detail"),
]
