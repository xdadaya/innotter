from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIClient
from tests.factories import UserFactory, PageFactory, PostFactory
from pytest_factoryboy import register
import pytest


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def anonymous_user():
    return AnonymousUser()


register(UserFactory)
register(PageFactory)
register(PostFactory)
