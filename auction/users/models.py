from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telephone = models.CharField(
        max_length=10,
        null=True,
        unique=True
    )

    class Meta:
        ordering = ['username', 'id']


class Avatar(models.Model):
    user = models.ForeignKey(User, related_name='avatar', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media', default='/users/base_icon.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return f"{self.user.username} avatar"
