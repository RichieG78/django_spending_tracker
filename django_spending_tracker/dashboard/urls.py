from django.urls import path
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
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'), #Changed here
    path('post/new/', PostCreateView.as_view(), name='post-create'), #url for creating a new post, changed here
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), #url for updating a post, changed here
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), #url for deleting a post, changed here
    path('about/',views.about, name='dashboard-about'),
]