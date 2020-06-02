from datetime import timedelta
from matplotlib import cm
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Lot(models.Model):
    heading = models.CharField(max_length=256)
    text_description = models.TextField()
    image = models.ImageField(upload_to='media', null=True)
    base_price = models.IntegerField(default=0)
    min_price_step = models.IntegerField(default=0)
    current_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now().replace(microsecond=0) + timedelta(days=3))
    author = models.ForeignKey(get_user_model(), related_name='lots', on_delete=models.CASCADE)
    is_mail_send = models.BooleanField(default=False)
    tags = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at', 'base_price']

    @property
    def is_available(self):
        return timezone.now() < self.expires_at

    @property
    def tags_list(self):
        return str(self.tags).split(';')

    @property
    def price(self):
        return self.base_price if self.base_price > self.current_price else self.current_price


class ImageTags(models.Model):
    lot = models.ForeignKey(Lot, related_name='img_tags', on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=50)
    confidence = models.FloatField(max_length=10)

    @property
    def color(self):
        cmap = cm.get_cmap('RdYlGn', 8)
        t = tuple(map(lambda x: x * 255, cmap(self.confidence)))
        return t


class Bet(models.Model):
    lot = models.ForeignKey(Lot, related_name='bets', on_delete=models.CASCADE)
    set_by = models.ForeignKey(get_user_model(), related_name='bets', on_delete=models.CASCADE)
    set_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'
