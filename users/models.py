from django.db import models
from users.managers import UserManager
from datetime import datetime, timedelta
from django.conf import settings
from users.userABC import UserABC
import jwt
import os
import uuid

class User(UserABC):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices, default="user")
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    objects = UserManager()

    @property
    def token(self) -> str:
        expires_at = datetime.now() + timedelta(days=int(os.environ.get("DELTA_DAYS_FOR_TOKEN_TO_EXPIRE")))
        token = jwt.encode({
            'id': self.pk,
            'exp': expires_at
        }, settings.SECRET_KEY, algorithm=os.environ.get("HASH_ALGORITHM"))
        return token

