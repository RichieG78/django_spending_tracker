"""Admin registrations for user profile data."""

from django.contrib import admin
from .models import Profile

# Show profile records in the admin alongside Django's built-in users.
admin.site.register(Profile)