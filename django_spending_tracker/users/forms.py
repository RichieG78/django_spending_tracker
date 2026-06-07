"""Forms used for registration, account updates, and preferences."""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm #Inheritance Relationship
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """Signup form that extends Django's default user creation form."""

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


#UserUpdateForm inherits from forms.ModelForm
class UserUpdateForm(forms.ModelForm):
    """Form for updating basic account fields shown in preferences."""

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Form for profile image and target percentage preferences."""

    class Meta:
        model = Profile 
        fields = ['image', 'fixed_target_percent', 'fun_target_percent', 'future_target_percent']

    def clean(self):
        """Ensure the three target percentages always total 100%."""
        cleaned_data = super().clean()
        fixed = cleaned_data.get('fixed_target_percent')
        fun = cleaned_data.get('fun_target_percent')
        future = cleaned_data.get('future_target_percent')

        if fixed is None or fun is None or future is None:
            return cleaned_data

        total = fixed + fun + future
        if total != 100:
            raise forms.ValidationError('Target percentages must add up to 100.')

        return cleaned_data