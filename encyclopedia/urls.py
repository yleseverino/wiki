from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_entry, name="random"),
    path("search", views.search_entry, name="search"),
    path("create_entry", views.create_entry, name="create_entry"),
    path("edit/<str:entry_name>", views.edit, name="edit"),
    path("<str:entry_name>", views.entry, name="entry")
]
