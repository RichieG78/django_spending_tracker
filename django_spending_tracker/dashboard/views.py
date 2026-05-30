from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Hello, world. You're at the spending tracker index.")

def about(request):
    return HttpResponse('<h1>Spending Tracker - About</h1>')