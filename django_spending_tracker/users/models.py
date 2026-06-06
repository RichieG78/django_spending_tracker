from pathlib import Path

from django.contrib.auth.models import User
from django.db import models
from PIL import Image, UnidentifiedImageError


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
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
