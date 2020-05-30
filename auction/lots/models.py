from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Lot(models.Model):
    heading = models.CharField(max_length=256)
    text_description = models.TextField()
    image = models.ImageField(upload_to='media', null=True)
    base_price = models.IntegerField(default=0)
    current_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now().replace(microsecond=0) + timedelta(days=3))
    author = models.ForeignKey(get_user_model(), related_name='lots', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at', 'base_price']


class Bet(models.Model):
    lot = models.ForeignKey(Lot, related_name='bets', on_delete=models.CASCADE)
    set_by = models.ForeignKey(get_user_model(), related_name='set_by_user', on_delete=models.CASCADE)
    set_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

