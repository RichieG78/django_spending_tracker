"""User profile model, including avatar and spending target preferences."""

from pathlib import Path

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image, UnidentifiedImageError


class Profile(models.Model):
    """Extra user data stored separately from Django's built-in User model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    # Target percentages used by the dashboard's Actual vs Target chart.
    fixed_target_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    fun_target_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=30,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    future_target_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """Save profile first, then safely resize uploaded profile images."""
        if self.image.name in {'default.jpg', 'media/profile_pics/default.jpg'}:
            self.image.name = 'profile_pics/default.jpg'

        super().save(*args, **kwargs)

        image_path = Path(self.image.path)
        if not image_path.exists():
            return

        try:
            with Image.open(image_path) as img:
                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))
                    img.save(image_path)
        except (UnidentifiedImageError, OSError):
            return
