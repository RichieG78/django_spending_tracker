from django.db.models.signals import post_save #This gets fired when a user is created
from django.contrib.auth.models import User #The user model will be the sender
from django.dispatch import receiver #We also need to import receiver
from .models import Profile #We want to import Profile from our models as we we will be creating a new profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Automatically create a profile when a new user account is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
   """Keep the related profile saved whenever the user record is saved."""
   instance.profile.save()