from users.models import User
from pages.models import Page
from users.serializers import UserSerializer
from datetime import date
import uuid


class UserService:
    @staticmethod
    def block(pk: uuid.UUID) -> None:
        User.objects.filter(id=pk).update(is_blocked=True)
        Page.objects.filter(owner=pk).update(unblock_date=date(9999, 1, 1))

    @staticmethod
    def unblock(pk: uuid.UUID) -> None:
        User.objects.filter(id=pk).update(is_blocked=False)

    @staticmethod
    def search(params: dict[str, str]) -> list[User]:
        users = User.objects.all()
        username = params.get("username", None)
        title = params.get("title", None)
        if username is not None:
            users = users.filter(username=username)
        if title is not None:
            users = users.filter(title=title)
        users = UserSerializer(users, many=True)
        return users.data
