from django.contrib.auth import get_user_model
from django.db import models

from users.models import User


class Lots(models.Model):
    heading = models.CharField(max_length=256)
    text_description = models.TextField()
    images = models.ImageField(upload_to='img')
    base_price = models.IntegerField()
    current_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(get_user_model(), related_name='Lots', on_delete=models.CASCADE)


class Bets(models.Model):
    lot = models.ForeignKey(Lots, related_name='bets', on_delete=models.CASCADE)
    set_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
