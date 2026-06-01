from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView

# Create your views here.
# def home(request):
#     context = {
#        'posts': Post.objects.all()
#     }
#     return render(request, 'dashboard/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'dashboard/home.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts' #<dashboard>/<post>_<list>.html, Now the default name is set equal to 'posts'
    ordering = ['-date_posted'] #Ordering the posts by date in descending order, - sign is used for descending order


class PostDetailView(DetailView):
    model = Post  


def about(request):
    return render(request, 'dashboard/about.html', {'title': 'About'})

