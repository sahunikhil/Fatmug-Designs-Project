from django.apps import AppConfig


class VmsPmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vms_pm'

    def ready(self):
        from . import signals
