from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
import jwt
import os


class UserABC(AbstractUser, PermissionsMixin):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'
    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    @property
    def token(self) -> str:
        expires_at = datetime.now() + timedelta(days=int(os.environ.get("DELTA_DAYS_FOR_TOKEN_TO_EXPIRE")))
        token = jwt.encode({
            'id': self.pk,
            'exp': expires_at
        }, settings.SECRET_KEY, algorithm=os.environ.get("HASH_ALGORITHM"))
        return token

    class Meta:
        abstract = True
