from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    DashboardView,
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
    path('add-expense/', views.add_expense, name='add_expense'),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),	name="password_reset_confirm"),
    path("reset/complete/", auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
    path('about/',views.about, name='dashboard-about'),
]