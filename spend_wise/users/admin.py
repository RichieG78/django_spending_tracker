"""Admin registrations for user profile data."""

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_currency', 'fixed_target_percent', 'fun_target_percent', 'future_target_percent')
    search_fields = ('user__username',)