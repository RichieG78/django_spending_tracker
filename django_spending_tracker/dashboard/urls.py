from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.home, name="dashboard-home"),
    path("about/", views.about, name="dashboard-about")
]