from django.contrib.auth import get_user_model
from django.db import models


class Lot(models.Model):
    heading = models.CharField(max_length=256)
    text_description = models.TextField()
    image = models.ImageField(upload_to='media', null=True)
    base_price = models.IntegerField(default=0)
    current_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)
    # user = models.ForeignKey(get_user_model(), related_name='lots', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at', 'base_price']


class Bet(models.Model):
    lot = models.ForeignKey(Lot, related_name='bets', on_delete=models.CASCADE)
    set_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
