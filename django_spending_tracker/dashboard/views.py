from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'Steve K',
        'title': 'First Blog Post',
        'content': 'Content for the first post.',
        'date_posted': '12/07/2023'
    },

     {
        'author': 'Scott K',
        'title': 'Second Blog Post',
        'content': 'Content for the second post.',
        'date_posted': '13/07/2023'
    }

] 

# Create your views here.
def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'dashboard/home.html', context)

def about(request):
    return render(request, 'dashboard/about.html', {'title': 'About'})

