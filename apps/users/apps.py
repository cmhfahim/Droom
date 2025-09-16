from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = "User Management"

    def ready(self):
        # Here you can import signals if any
        # from . import signals
        pass
