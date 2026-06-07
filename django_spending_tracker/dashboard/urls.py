"""URL routes for dashboard, spending tracker, and finance CRUD views."""

from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .views import (
    DashboardView,
    SpendingTrackerView,
    ExpenseDetailView,
    ExpenseUpdateView,
    ExpenseDeleteView,
    FixedExpenseCreateView,
    FunExpenseCreateView,
    FutureExpenseCreateView,
    IncomeCreateView,
    IncomeDetailView,
    IncomeUpdateView,
    IncomeDeleteView,
)
from . import views

# Each path below maps a browser URL to one page/action in the dashboard app.
urlpatterns = [
    # Main dashboard with income summary and target chart.
    path('', DashboardView.as_view(), name='dashboard-home'),

    # Dedicated page for all expense tracking functionality.
    path('spending-tracker/', SpendingTrackerView.as_view(), name='spending-tracker'),

    # Backward-compatible route for previous nav label/path.
    path('performance/', RedirectView.as_view(pattern_name='spending-tracker', permanent=False)),

    # Income CRUD pages.
    path('add-income/', IncomeCreateView.as_view(), name='add_income'),
    path('income/<int:pk>/', IncomeDetailView.as_view(), name='income-detail'),
    path('income/<int:pk>/update/', IncomeUpdateView.as_view(), name='income-update'),
    path('income/<int:pk>/delete/', IncomeDeleteView.as_view(), name='income-delete'),

    # Fixed expense CRUD pages.
    path('expenses/fixed/add/', FixedExpenseCreateView.as_view(), name='add_fixed_expense'),
    path('expenses/fixed/<int:pk>/', ExpenseDetailView.as_view(expense_type='fixed'), name='expense-fixed-detail'),
    path('expenses/fixed/<int:pk>/update/', ExpenseUpdateView.as_view(expense_type='fixed'), name='expense-fixed-update'),
    path('expenses/fixed/<int:pk>/delete/', ExpenseDeleteView.as_view(expense_type='fixed'), name='expense-fixed-delete'),

    # Fun expense CRUD pages.
    path('expenses/fun/add/', FunExpenseCreateView.as_view(), name='add_fun_expense'),
    path('expenses/fun/<int:pk>/', ExpenseDetailView.as_view(expense_type='fun'), name='expense-fun-detail'),
    path('expenses/fun/<int:pk>/update/', ExpenseUpdateView.as_view(expense_type='fun'), name='expense-fun-update'),
    path('expenses/fun/<int:pk>/delete/', ExpenseDeleteView.as_view(expense_type='fun'), name='expense-fun-delete'),

    # Future expense CRUD pages.
    path('expenses/future/add/', FutureExpenseCreateView.as_view(), name='add_future_expense'),
    path('expenses/future/<int:pk>/', ExpenseDetailView.as_view(expense_type='future'), name='expense-future-detail'),
    path('expenses/future/<int:pk>/update/', ExpenseUpdateView.as_view(expense_type='future'), name='expense-future-update'),
    path('expenses/future/<int:pk>/delete/', ExpenseDeleteView.as_view(expense_type='future'), name='expense-future-delete'),

    # Backward-compatible expense routes that point to fixed expense views.
    path('add-expense/', FixedExpenseCreateView.as_view(), name='add_expense'),
    path('expense/<int:pk>/', ExpenseDetailView.as_view(expense_type='fixed'), name='expense-detail'),
    path('expense/<int:pk>/update/', ExpenseUpdateView.as_view(expense_type='fixed'), name='expense-update'),
    path('expense/<int:pk>/delete/', ExpenseDeleteView.as_view(expense_type='fixed'), name='expense-delete'),

    # Password reset flow pages (handled by Django auth views).
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),	name="password_reset_confirm"),
    path("reset/complete/", auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),

    # Static about page.
    path('about/',views.about, name='dashboard-about'),
]