from django.apps import AppConfig


class SaroxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sarox"
    
    def ready(self):
        import sarox.signals  # This is where you import your signals file
