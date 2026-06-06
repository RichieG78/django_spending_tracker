from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    DashboardView,
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
from .import views

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard-home'), #Changed here
    path('add-income/', IncomeCreateView.as_view(), name='add_income'),
    path('income/<int:pk>/', IncomeDetailView.as_view(), name='income-detail'),
    path('income/<int:pk>/update/', IncomeUpdateView.as_view(), name='income-update'),
    path('income/<int:pk>/delete/', IncomeDeleteView.as_view(), name='income-delete'),
    path('expenses/fixed/add/', FixedExpenseCreateView.as_view(), name='add_fixed_expense'),
    path('expenses/fixed/<int:pk>/', ExpenseDetailView.as_view(expense_type='fixed'), name='expense-fixed-detail'),
    path('expenses/fixed/<int:pk>/update/', ExpenseUpdateView.as_view(expense_type='fixed'), name='expense-fixed-update'),
    path('expenses/fixed/<int:pk>/delete/', ExpenseDeleteView.as_view(expense_type='fixed'), name='expense-fixed-delete'),
    path('expenses/fun/add/', FunExpenseCreateView.as_view(), name='add_fun_expense'),
    path('expenses/fun/<int:pk>/', ExpenseDetailView.as_view(expense_type='fun'), name='expense-fun-detail'),
    path('expenses/fun/<int:pk>/update/', ExpenseUpdateView.as_view(expense_type='fun'), name='expense-fun-update'),
    path('expenses/fun/<int:pk>/delete/', ExpenseDeleteView.as_view(expense_type='fun'), name='expense-fun-delete'),
    path('expenses/future/add/', FutureExpenseCreateView.as_view(), name='add_future_expense'),
    path('expenses/future/<int:pk>/', ExpenseDetailView.as_view(expense_type='future'), name='expense-future-detail'),
    path('expenses/future/<int:pk>/update/', ExpenseUpdateView.as_view(expense_type='future'), name='expense-future-update'),
    path('expenses/future/<int:pk>/delete/', ExpenseDeleteView.as_view(expense_type='future'), name='expense-future-delete'),
    path('add-expense/', FixedExpenseCreateView.as_view(), name='add_expense'),
    path('expense/<int:pk>/', ExpenseDetailView.as_view(expense_type='fixed'), name='expense-detail'),
    path('expense/<int:pk>/update/', ExpenseUpdateView.as_view(expense_type='fixed'), name='expense-update'),
    path('expense/<int:pk>/delete/', ExpenseDeleteView.as_view(expense_type='fixed'), name='expense-delete'),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),	name="password_reset_confirm"),
    path("reset/complete/", auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
    path('about/',views.about, name='dashboard-about'),
]