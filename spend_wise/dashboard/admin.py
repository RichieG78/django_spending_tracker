"""Admin registrations for dashboard data models."""

from django.contrib import admin
from .models import Expense, Income


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'currency', 'type', 'frequency', 'date', 'user')
    list_filter = ('type', 'frequency')
    search_fields = ('name', 'user__username')


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'currency', 'type', 'frequency', 'gross_net', 'date', 'user')
    list_filter = ('type', 'frequency')
    search_fields = ('name', 'user__username')

