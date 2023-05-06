import pytest
from faker import Faker

from pages.page_service import PageService
from posts.models import Like
from posts.post_service import PostService
from posts.serializers import PostSerializer
from tests.factories import UserFactory, PostFactory, PageFactory


@pytest.mark.django_db
def test_like_post(user_factory: UserFactory, post_factory: PostFactory) -> None:
    faker = Faker()
    user = user_factory.create(username=faker.name(), email=faker.email())
    post = post_factory.create()
    PostService.like(post.id, user)
    post.refresh_from_db()
    assert post.likes_amount == 1
    assert Like.objects.filter(post=post, user=user).count() == 1
    PostService.like(post.id, user)
    post.refresh_from_db()
    assert post.likes_amount == 1
    assert Like.objects.filter(post=post, user=user).count() == 1


@pytest.mark.django_db
def test_unlike_post(user_factory: UserFactory, post_factory: PostFactory) -> None:
    faker = Faker()
    user = user_factory.create(username=faker.name(), email=faker.email())
    post = post_factory.create()
    PostService.like(post.id, user)
    post.refresh_from_db()
    assert post.likes_amount == 1
    assert Like.objects.filter(post=post, user=user).count() == 1
    PostService.dislike(post.id, user)
    post.refresh_from_db()
    assert post.likes_amount == 0
    assert Like.objects.filter(post=post, user=user).count() == 0


@pytest.mark.django_db
def test_feed(user_factory: UserFactory, post_factory: PostFactory, page_factory: PageFactory) -> None:
    faker = Faker()
    user = user_factory.create(username=faker.name(), email=faker.email())
    page1 = page_factory.create()
    page2 = page_factory.create(owner=user)
    PageService.follow(user, page1.id)
    post1 = post_factory.create(page=page1)
    post2 = post_factory.create(page=page2)
    feed = PostService.feed(user)
    assert len(feed) == 2


@pytest.mark.django_db
def test_liked(user_factory: UserFactory, post_factory: PostFactory, page_factory: PageFactory) -> None:
    faker = Faker()
    user = user_factory.create()
    page = page_factory.create(owner=user)
    post1 = post_factory.create(page=page)
    post2 = post_factory.create(page=page)
    post3 = post_factory.create(page=page)
    post4 = post_factory.create(page=page)
    PostService.like(post2.id, user)
    PostService.like(post4.id, user)
    liked = PostService.liked(user)
    post2.refresh_from_db()
    post4.refresh_from_db()
    assert len(liked) == 2
    assert liked == PostSerializer([post2, post4], many=True).data
