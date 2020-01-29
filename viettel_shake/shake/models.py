from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class ViettelUser(models.Model):
    phone = PhoneNumberField(
        null=False,
        blank=False,
        unique=True
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return '{} - {}'.format(self.phone, self.created_at)


class GiftManager(models.Manager):
    def get_queryset(self):
        query = \
            Q(data__status__code='SG0005') \
            | Q(data__status__code='SG0020') \
            | Q(data__status__code='SG0021') \
            | Q(data__status__code='SG0023') \
            | Q(data__status__code='SG0099')
        return super().get_queryset().exclude(query)


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

    objects = models.Manager()
    gifts = GiftManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return '{} - {}'.format(self.user.phone, self.data['status']['message'])
