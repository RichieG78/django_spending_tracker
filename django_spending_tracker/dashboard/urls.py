from django.urls import path
from .views import PostListView, PostDetailView #Changed here
from .import views

urlpatterns = [
    path('', PostListView.as_view(), name='dashboard-home'), #Changed here
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'), #Changed here
    path('about/',views.about, name='dashboard-about'),
]