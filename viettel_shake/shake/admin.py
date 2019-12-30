from django.contrib import admin
from django.contrib.postgres.fields import JSONField

from viettel_shake.utils.widgets import PrettyJSONWidget
from .models import Shake, ViettelUser


class ShakeAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('user')

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }


admin.site.register(ViettelUser)
admin.site.register(Shake, ShakeAdmin)
