"""Validation tests for user-facing account and profile forms."""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


class UserFormTests(TestCase):
    """Exercise the custom registration and profile forms with common inputs."""

    def setUp(self):
        """Create one baseline user and profile for profile-update scenarios."""
        self.user = User.objects.create_user(username='testuser', password='12345')
        # The post-save signal creates the related profile automatically.
        self.user.profile.image = 'default.png'
        self.user.profile.save()

    def test_user_register_form(self):
        """Registration form should accept a valid new user payload."""
        form_data = {
            'username': 'newuser', 
            'email': 'newuser@example.com', 
            'password1': 'django1234', 
            'password2': 'django1234'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_update_form(self):
        """Updating username and email should be valid and persist to the user record."""
        form_data = {
            'username': 'updateduser', 
            'email': 'updateduser@example.com'
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_profile_update_with_invalid_image_format(self):
        """Profile form should reject uploads that are not real images."""
        invalid_image_data = b'this is not real image data'
        invalid_image_file = SimpleUploadedFile('new_image.txt', invalid_image_data, content_type='text/plain')
        form = ProfileUpdateForm(files={'image': invalid_image_file}, instance=self.user.profile)
        self.assertFalse(form.is_valid())
    
    def test_profile_update_with_oversized_image(self):
        """Profile form should reject very large uploads before saving them."""
        oversized_image_data = b'\x00' * 5242880  # 5MB of zeros
        oversized_image_file = SimpleUploadedFile('new_image.jpg', oversized_image_data, content_type='image/jpeg')
        form = ProfileUpdateForm(files={'image': oversized_image_file}, instance=self.user.profile)
        self.assertFalse(form.is_valid())