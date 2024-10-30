from django.db import models
from django.utils import timezone
from datetime import timedelta

class SerialKey(models.Model):
    serial_key = models.CharField(max_length=100, unique=True)

class Subscription(models.Model):
    serial_key = models.ForeignKey(SerialKey, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    last_checkin = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
