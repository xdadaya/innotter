from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from users.managers import UserManager
from datetime import datetime, timedelta
from django.conf import settings
import jwt
import os


class User(AbstractUser, PermissionsMixin):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'
    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    objects = UserManager()

    @property
    def token(self) -> str:
        exp_dt = datetime.now() + timedelta(days=os.environ.get("DELTA_DAYS_FOR_TOKEN_TO_EXPIRE"))
        token = jwt.encode({
            'id': self.pk,
            'exp': exp_dt
        }, settings.SECRET_KEY, algorithm=os.environ.get("HASH_ALGORITHM"))
        return token

