from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin #Added here to restrict access to certain views to logged in users only
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView, #Added here, note if you have a long line of imports you can add ( ) to move each to a new line
    DeleteView #Added here for delete view
)

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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
     
    #Overriding form_valid method 
    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author on the form
        return super().form_valid(form) # Validate form by running form_valid method from parent class.
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    #Overriding form_valid method 
    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author on the form
        return super().form_valid(form) # Validate form by running form_valid method from parent class.
    
    #Added a new function here to check the user author is correct for the specific Post.
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # New class PostDeleteView created here
    model = Post
    success_url = '/' # After deleting a post, the user will be redirected to the home page.
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
def about(request):
    return render(request, 'dashboard/about.html', {'title': 'About'})

