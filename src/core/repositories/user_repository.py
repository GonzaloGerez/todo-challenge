from typing import Optional
from django.contrib.auth.hashers import make_password
from src.authentication.models import User
from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    """
    Repository for User model operations.
    Handles all database operations related to users.
    """
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email address."""
        return self.get_first(email=email)
    
    def create_user(self, email: str, password: str, first_name: str = '', last_name: str = '') -> User:
        """Create a new user with hashed password."""
        return self.create(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name
        )
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        return self.exists(email=email)
