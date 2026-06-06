from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from .import views

urlpatterns = [
    path('', PostListView.as_view(), name='dashboard-home'), #Changed here
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'), #Changed here
    path('post/new/', PostCreateView.as_view(), name='post-create'), #url for creating a new post, changed here
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), #url for updating a post, changed here
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), #url for deleting a post, changed here
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),	name="password_reset_confirm"),
    path("reset/complete/", auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
    path('about/',views.about, name='dashboard-about'),
]