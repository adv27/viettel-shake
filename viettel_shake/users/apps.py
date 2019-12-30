from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "viettel_shake.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import viettel_shake.users.signals  # noqa F401
        except ImportError:
            pass
