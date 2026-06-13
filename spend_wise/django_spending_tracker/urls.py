"""
URL configuration for django_spending_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('app/', include('app.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views

# Project URL map: this connects top-level website paths to app pages.
urlpatterns = [
    # Django admin site.
    path('admin/', admin.site.urls),

    # Main application routes from the dashboard app.
    path('', include("dashboard.urls")),

    # Authentication and account routes.
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', extra_context={'show_sidebar': False}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html', extra_context={'show_sidebar': False}), name='logout'),

    # Preferences/profile routes for logged-in users.
    path('preferences/', user_views.preferences, name='preferences'),
    path('profile/', user_views.profile, name='profile'),
]

# In development, let Django serve uploaded media directly.
# In production, media should be served by the hosting platform/storage layer.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)