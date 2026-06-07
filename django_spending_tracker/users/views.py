"""Views for account signup and user preference management."""

from urllib import request

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm #Import added
from django.contrib.auth.decorators import login_required #Import added

# Create your views here.
def register(request):
    """Register a new user account, then send the user to the login page."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) #UserRegisterForm instead of UserCreationForm
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully, now you can login.')
            return redirect('login')
    else:
        form = UserRegisterForm() #UserRegisterForm instead of UserCreationForm
    return render(request, 'users/register.html', {'form': form, 'show_sidebar': False})


@login_required # Added decorator here
def preferences(request):
    """Edit account/profile details and chart target preferences on one page."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your preferences have been updated!')
            return redirect('preferences')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def profile(request):
    """Legacy profile route kept as a friendly redirect to preferences."""
    return redirect('preferences')

