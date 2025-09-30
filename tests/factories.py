"""
Factories for generating test data using factory_boy.
"""
import os
import factory
import django
from django.conf import settings

# Set Django settings module before importing Django modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.todo_api.test_settings')

# Configure Django settings before importing Django modules
if not settings.configured:
    django.setup()

from django.contrib.auth import get_user_model
from src.authentication.models import User
from src.core.models import Task

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances."""
    
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_superuser = False


class TaskFactory(factory.django.DjangoModelFactory):
    """Factory for creating Task instances."""
    
    class Meta:
        model = Task
    
    detail = factory.Faker('sentence', nb_words=6)
    status = factory.Iterator(['pending', 'completed', 'cancelled'])
    user = factory.SubFactory(UserFactory)
