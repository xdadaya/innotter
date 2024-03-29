import uuid
from datetime import date

from pages.models import Page
from users.models import User


class UserService:
    @staticmethod
    def block(pk: uuid.UUID) -> None:
        User.objects.filter(id=pk).update(is_blocked=True)
        Page.objects.filter(owner=pk).update(unblock_date=date(9999, 1, 1))

    @staticmethod
    def unblock(pk: uuid.UUID) -> None:
        User.objects.filter(id=pk).update(is_blocked=False)

    @staticmethod
    def change_role(pk: uuid.UUID, role: str) -> None:
        User.objects.filter(id=pk).update(role=role)
