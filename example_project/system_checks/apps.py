from django.apps import AppConfig


class SystemChecksConfig(AppConfig):
    name = 'system_checks'

    def ready(self):
        from .checks import example_check  # noqa
