"""Admin registrations for dashboard data models."""

from django.contrib import admin
from .models import Expense, Income

# Expose both finance models in the Django admin for quick inspection.
admin.site.register(Income)
admin.site.register(Expense)

