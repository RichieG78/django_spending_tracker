from urllib import request

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm  #Import added
from django.contrib.auth.decorators import login_required #Import added

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) #UserRegisterForm instead of UserCreationForm
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully, now you can login.')
        return redirect('login') 
    else:
        form = UserRegisterForm() #UserRegisterForm instead of UserCreationForm
    return render(request, 'users/register.html', {'form': form})

@login_required # Added decorator here
def profile(request):
    return render(request, 'users/profile.html')

