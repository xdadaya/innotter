from django.db import models
from users.managers import UserManager
from users.userABC import UserABC
from users.token_service import TokenService
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
        return TokenService.generate_token(self.id)

