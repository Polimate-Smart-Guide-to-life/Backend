from factory.django import DjangoModelFactory
from factory.faker import Faker

from apps.users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    email = Faker("email")