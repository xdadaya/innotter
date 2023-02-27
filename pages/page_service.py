from users.models import User
from users.serializers import UserSerializer
from pages.models import Page, FollowRequest
from tags.models import Tag
from pages.serializers import PageSerializer
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
import uuid


class PageService:
    @staticmethod
    def follow(user: User, pk: uuid.UUID) -> None:
        page = Page.objects.get(id=pk)
        if page.is_private and not page.followers.filter(username=user.username).exists():
            FollowRequest.objects.create(follower=user, page=page)
        else:
            page.followers.add(user)

    @staticmethod
    def unfollow(user: User, pk: uuid.UUID) -> None:
        page = Page.objects.get(id=pk)
        page.followers.remove(user)
        FollowRequest.objects.filter(follower=user, page=page).delete()


    @staticmethod
    def accept_all_requests(pk: uuid.UUID) -> None:
        page = Page.objects.get(id=pk)
        for request in FollowRequest.objects.filter(page=page):
            page.followers.add(request.follower)
        FollowRequest.objects.filter(page=page).delete()

    @staticmethod
    def reject_all_requests(pk: uuid.UUID) -> None:
        page = Page.objects.get(id=pk)
        FollowRequest.objects.filter(page=page).delete()

    @staticmethod
    def accept_single_request(pk: uuid.UUID, request_id: uuid.UUID) -> None:
        page = Page.objects.get(id=pk)
        request = get_object_or_404(FollowRequest, id=request_id)
        page.followers.add(request.follower)
        request.delete()

    @staticmethod
    def reject_single_request(request_id: uuid.UUID) -> None:
        FollowRequest.objects.filter(id=request_id).delete()

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

    @staticmethod
    def block_page_permanent(pk: uuid.UUID) -> None:
        Page.objects.filter(id=pk).update(unblock_date=date(9999, 1, 1))
