import factory
from faker import Faker

from pages.models import Page
from posts.models import Post
from users.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    username = fake.first_name()
    password = fake.password()
    email = fake.email()

    class Meta:
        model = User


class PageFactory(factory.django.DjangoModelFactory):
    name = fake.name()
    description = fake.text()
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Page


class PostFactory(factory.django.DjangoModelFactory):
    content = fake.name()
    page = factory.SubFactory(PageFactory)

    class Meta:
        model = Post
