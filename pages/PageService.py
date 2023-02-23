from users.models import User
from users.serializers import UserSerializer
from pages.models import Page
from datetime import date, timedelta
import uuid


class PageService:
    @staticmethod
    def follow(user: User, pk: uuid.UUID) -> None:
        page = Page.objects.get(id=pk)
        if page.is_private and user not in page.followers.all():
            page.follow_requests.add(user)
        else:
            page.followers.add(user)

    @staticmethod
    def accept_all_requests(pk: uuid.UUID) -> None:
        page = Page.objects.get(id=pk)
        all_follow_requests = page.follow_requests.all()
        for request in all_follow_requests:
            page.followers.add(request)
        page.follow_requests.clear()

    @staticmethod
    def accept_single_request(pk: uuid.UUID, user_id: uuid.UUID) -> None:
        page = Page.objects.get(id=pk)
        user = User.objects.get(id=user_id)
        if user in page.follow_requests.all():
            page.follow_requests.remove(user)
            page.followers.add(user)

    @staticmethod
    def follow_requests(pk: uuid.UUID) -> list[User]:
        page = Page.objects.get(id=pk)
        users = UserSerializer(page.follow_requests.all(), many=True)
        return users.data

    @staticmethod
    def set_private(pk: uuid.UUID) -> None:
        Page.objects.filter(id=pk).update(is_private=True)

    @staticmethod
    def set_public(pk: uuid.UUID) -> None:
        Page.objects.filter(id=pk).update(is_private=False)

    @staticmethod
    def block_page(pk: uuid.UUID, delta_days: int) -> None:
        Page.objects.filter(id=pk).update(unblock_date=date.today()+timedelta(days=int(delta_days)))
