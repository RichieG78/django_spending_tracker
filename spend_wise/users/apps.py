"""App configuration for the users module."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Register the users app and connect its signal handlers."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """Import signal handlers once Django has loaded the app registry."""
        import users.signals