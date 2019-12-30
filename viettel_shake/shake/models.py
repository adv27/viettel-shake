from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class ViettelUser(models.Model):
    phone = PhoneNumberField(
        null=False,
        blank=False,
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.phone)


class Shake(models.Model):
    """
    Model for holding data response of shake action
    """
    user = models.ForeignKey(
        'ViettelUser',
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='shakes'
    )
    data = JSONField()
    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return '{} - {}'.format(self.user.phone, self.data['status']['message'])
