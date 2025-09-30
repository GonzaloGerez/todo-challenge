"""
Pytest configuration and fixtures.
"""
import os
import pytest
import django
from django.conf import settings

# Set Django settings module before importing Django modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.todo_api.test_settings')

# Configure Django settings before importing Django modules
if not settings.configured:
    django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from tests.factories import UserFactory

User = get_user_model()


@pytest.fixture
def client():
    """Django test client fixture."""
    return Client()


@pytest.fixture
def user():
    """User fixture."""
    return UserFactory()


@pytest.fixture
def authenticated_client(client, user):
    """Authenticated client fixture."""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    return client


@pytest.fixture
def other_user():
    """Other user fixture for testing permissions."""
    return UserFactory()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests."""
    pass
