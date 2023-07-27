from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>", views.page, name="page"),
    path("edit/<str:title>", views.edit, name="edit")
]
