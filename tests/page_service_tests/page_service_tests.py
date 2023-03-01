from tests.factories import UserFactory, PageFactory
from pages.page_service import PageService
from pages.models import Page, FollowRequest
from users.models import User
from datetime import datetime, timedelta, date
from pytz import utc
from faker import Faker
import pytest


@pytest.mark.django_db
def test_follow_public_page_valid(user_factory: UserFactory, page_factory: PageFactory) -> None:
    faker = Faker()
    user = user_factory.create(username=faker.name(), email=faker.email())
    page = page_factory.create(is_private=False)
    PageService.follow(user, page.id)
    assert Page.objects.filter(id=page.id, followers__id__exact=user.id).count() == 1
    assert FollowRequest.objects.filter(page=page, follower=user).count() == 0


@pytest.mark.django_db
def test_follow_private_page_valid(user_factory: UserFactory, page_factory: PageFactory) -> None:
    faker = Faker()
    user = user_factory.create(username=faker.name(), email=faker.email())
    page = page_factory.create(is_private=True)
    PageService.follow(user, page.id)
    assert Page.objects.filter(id=page.id, followers__id__exact=user.id).count() == 0
    assert FollowRequest.objects.filter(page=page, follower=user).count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    'is_page_private', (True, False)
)
def test_unfollow_page_valid(user_factory: UserFactory, page_factory: PageFactory, is_page_private) -> None:
    faker = Faker()
    user = user_factory.create(username=faker.name(), email=faker.email())
    page = page_factory.create(is_private=is_page_private)
    PageService.follow(user, page.id)
    PageService.unfollow(user, page.id)
    assert Page.objects.filter(id=page.id, followers__id__exact=user.id).count() == 0
    assert FollowRequest.objects.filter(page=page, follower=user).count() == 0


@pytest.mark.django_db
def test_accept_all_follow_requests(user_factory: UserFactory, page_factory: PageFactory) -> None:
    page = page_factory.create(is_private=True)
    faker = Faker()
    for _ in range(3):
        user = user_factory.create(username=faker.name(), email=faker.email())
        PageService.follow(user, page.id)
    assert FollowRequest.objects.filter(page=page).count() == 3
    PageService.accept_all_requests(page.id)
    assert FollowRequest.objects.filter(page=page).count() == 0
    assert Page.objects.get(id=page.id).followers.count() == 3


@pytest.mark.django_db
def test_accept_single_follow_requests(user_factory: UserFactory, page_factory: PageFactory) -> None:
    page = page_factory.create(is_private=True)
    faker = Faker()
    for _ in range(3):
        user = user_factory.create(username=faker.name(), email=faker.email())
        PageService.follow(user, page.id)
    follower_user = User.objects.first()
    assert FollowRequest.objects.filter(page=page).count() == 3
    PageService.accept_single_request(page.id, FollowRequest.objects.get(follower=follower_user).id)
    assert FollowRequest.objects.filter(page=page).count() == 2
    assert Page.objects.get(id=page.id).followers.count() == 1
    assert Page.objects.filter(id=page.id, followers__id__exact=follower_user.id).count() == 1


@pytest.mark.django_db
def test_reject_single_follow_requests(user_factory: UserFactory, page_factory: PageFactory) -> None:
    page = page_factory.create(is_private=True)
    faker = Faker()
    for _ in range(3):
        user = user_factory.create(username=faker.name(), email=faker.email())
        PageService.follow(user, page.id)
    follower_user = User.objects.first()
    assert FollowRequest.objects.filter(page=page).count() == 3
    PageService.reject_single_request(page.id, FollowRequest.objects.get(follower=follower_user).id)
    assert FollowRequest.objects.filter(page=page).count() == 2
    assert Page.objects.get(id=page.id).followers.count() == 0
    assert Page.objects.filter(id=page.id, followers__id__exact=follower_user.id).count() == 0


@pytest.mark.django_db
def test_reject_all_follow_requests(user_factory: UserFactory, page_factory: PageFactory) -> None:
    page = page_factory.create(is_private=True)
    faker = Faker()
    for _ in range(3):
        user = user_factory.create(username=faker.name(), email=faker.email())
        PageService.follow(user, page.id)
    assert FollowRequest.objects.filter(page=page).count() == 3
    PageService.reject_all_requests(page.id)
    assert FollowRequest.objects.filter(page=page).count() == 0
    assert Page.objects.get(id=page.id).followers.count() == 0


@pytest.mark.django_db
def test_set_private_page(page_factory: PageFactory) -> None:
    page = page_factory.create(is_private=False)
    PageService.set_private(page.id)
    page.refresh_from_db()
    assert page.is_private == True


@pytest.mark.django_db
def test_set_public_page(page_factory: PageFactory) -> None:
    page = page_factory.create(is_private=True)
    PageService.set_public(page.id)
    page.refresh_from_db()
    assert page.is_private == False


@pytest.mark.django_db
def test_blocking_page(page_factory: PageFactory) -> None:
    page = page_factory.create()
    PageService.block_page(page.id, 10)
    page.refresh_from_db()
    date_now = date.today()
    unblock_date = datetime(date_now.year, date_now.month, date_now.day) + timedelta(days=10)
    unblock_date = utc.localize(unblock_date)
    assert page.unblock_date == unblock_date


@pytest.mark.django_db
def test_permanent_blocking_page(page_factory: PageFactory) -> None:
    page = page_factory.create()
    PageService.block_page_permanent(page.id)
    page.refresh_from_db()
    assert page.unblock_date == utc.localize(datetime(9999, 1, 1))
