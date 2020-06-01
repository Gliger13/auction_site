import base64
import datetime
import hashlib
import random
import string

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.db import models
from django.utils import timezone

from auction import settings
from auction.settings import HOST


class User(AbstractUser):
    TOKEN_ALPHABET = (string.ascii_letters + string.digits) * 10
    TOKEN_LENGTH = 256

    signer = TimestampSigner()

    username = models.CharField(
        unique=True,
        max_length=15,
    )
    first_name = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )
    second_name = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )
    telephone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        unique=True,
    )
    # For email verification
    is_email_verified = models.BooleanField(default=False)
    secret_email_token = models.CharField(max_length=TOKEN_LENGTH)
    verification_email_sent_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['username', 'id']

    @property
    def days_after_reg(self):
        all_time = timezone.now() - self.date_joined
        return all_time.days

    @property
    def hidden_email(self):
        end_suffix = self.email.split('.')[-1]
        email = self.email.split('.')[:-1][0]
        hidden_email = '**'.join(email[::3])
        return hidden_email + '.' + end_suffix

    @property
    def hidden_telephone(self):
        if self.telephone:
            hidden_telephone = self.telephone[:3] + '**'.join(self.telephone[3::3])
            return hidden_telephone
        else:
            return None

    @property
    def lots_count(self):
        return self.lots.count

    @property
    def bets_count(self):
        return self.bets.count

    def get_secret_token(self):
        return "".join(
            random.sample(self.TOKEN_ALPHABET, self.TOKEN_LENGTH)
        )

    def digest_token(self, token):
        return hashlib.md5(
            token.encode('utf-8')
        ).hexdigest()

    def sign_token(self, token):
        return self.signer.sign(token)

    def unsign_token(self, token):
        return self.signer.unsign(token, max_age=datetime.timedelta(hours=2))

    def convert_token(self, token):
        return base64.b64encode(token.encode('utf-8')).decode('utf-8')

    def make_verify_link(self, token):
        return f"{HOST}/verify/?token={token}"

    def deconvert_token(self, token):
        return base64.b64decode(token.encode('utf-8')).decode('utf-8')

    def is_token_correct(self, token):
        deconverted = self.deconvert_token(token)
        unsigned = self.unsign_token(deconverted)
        return unsigned == self.digest_token(self.secret_email_token)

    def verify_email(self):
        self.is_email_verified = True
        self.save()

    def send_verification_email(self):
        token = self.get_secret_token()
        self.secret_email_token = token
        self.verification_email_sent_at = timezone.now()
        self.save()

        digested_token = self.digest_token(token)
        signed = self.sign_token(digested_token)
        converted = self.convert_token(signed)
        link = self.make_verify_link(converted)

        return send_mail(
            "Verify your email",
            f"Please follow this link: {link}",
            settings.ADMIN_EMAIL,
            [self.email]
        )


class Avatar(models.Model):
    user = models.OneToOneField(
        User,
        related_name='avatar',
        on_delete=models.CASCADE,
        unique=True
    )
    image = models.ImageField(
        upload_to='media',
        default='users/base_icon.jpg'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return f"{self.user.username} avatar"
