from django.apps import AppConfig


class AccountModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account_module'

    def ready(self):
        import account_module.signals
