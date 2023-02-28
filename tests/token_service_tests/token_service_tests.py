from tests.factories import UserFactory
from users.token_service import TokenService
from innotter import settings
import pytest


@pytest.mark.django_db
def test_generate_token(user_factory: UserFactory) -> None:
    user = user_factory.create()
    token = TokenService.generate_token(user.id)
    assert token
    assert len(token.split(".")) == 3


@pytest.mark.django_db
def test_verify_token(user_factory: UserFactory) -> None:
    user = user_factory.create()
    token = TokenService.generate_token(user.id)
    bearer_token = f"{settings.AUTHENTICATION_HEADER_PREFIX} {token}"
    verified_token = TokenService.verify_token(bearer_token.split())
    assert verified_token
    assert token==verified_token
