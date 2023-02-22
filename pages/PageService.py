from users.models import User
from users.serializers import UserSerializer
from django.http import HttpRequest
from pages.models import Page
from datetime import date, timedelta

class PageService:
    @staticmethod
    def follow(request: HttpRequest, pk: int) -> None:
        page = Page.objects.get(id=pk)
        if page.is_private:
            page.follow_requests.add(request.user)
        else:
            page.followers.add(request.user)

    @staticmethod
    def acceptAllRequests(request: HttpRequest, pk: int) -> None:
        page = Page.objects.get(id=pk)
        all_follow_requests = list(page.follow_requests.all())
        for request in all_follow_requests:
            page.followers.add(request)
        page.follow_requests.clear()

    @staticmethod
    def acceptSingleRequest(request: HttpRequest, pk: int, user_id: int) -> None:
        page = Page.objects.get(id=pk)
        user = User.objects.get(id=user_id)
        if user in page.follow_requests.all():
            page.follow_requests.remove(user)
            page.followers.add(user)

    @staticmethod
    def followRequests(pk: int) -> list[User]:
        page = Page.objects.get(id=pk)
        print(page.follow_requests.all())
        users = UserSerializer(page.follow_requests.all(), many=True)
        return users.data

    @staticmethod
    def setPrivate(pk: int) -> None:
        Page.objects.filter(id=pk).update(is_private=True)

    @staticmethod
    def setPublic(pk: int) -> None:
        Page.objects.filter(id=pk).update(is_private=False)

    @staticmethod
    def blockPage(pk: int, delta_days: int) -> None:
        Page.objects.filter(id=pk).update(unblock_date=date.today()+timedelta(days=int(delta_days)))
