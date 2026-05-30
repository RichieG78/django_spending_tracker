from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.home, name="dashboard"),
    path("about/", views.about, name="dashboard_about")
]