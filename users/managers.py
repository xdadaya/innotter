from django.contrib.auth.base_user import BaseUserManager
from users.userABC import UserABC


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str, password: str) -> UserABC:
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, email: str, password: str) -> UserABC:
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username, email, password)
        user.role = "admin"
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
