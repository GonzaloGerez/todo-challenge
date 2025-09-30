from typing import Dict, Any, Optional
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from src.authentication.models import User
from ..repositories.user_repository import UserRepository
from .base_service import BaseService


class UserService(BaseService):
    """
    Service class for user-related business logic.
    Handles user registration and authentication.
    """
    
    def __init__(self):
        self.user_repository = UserRepository()
    
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new user.
        
        Args:
            user_data: Dictionary containing user information (email, password, first_name, last_name)
            
        Returns:
            Dictionary with success status and user data or error message
        """
        try:
            # Validate required fields
            required_fields = ['email', 'password', 'first_name', 'last_name']
            self.validate_required_fields(user_data, required_fields)
            
            # Validate email format
            if not self.validate_email_format(user_data['email']):
                raise ValidationError("Invalid email format")
            
            # Validate password strength
            if not self.validate_password_strength(user_data['password']):
                raise ValidationError("Password must be at least 8 characters long")
            
            # Check if email already exists
            if self.user_repository.email_exists(user_data['email']):
                raise ValidationError("User with this email already exists")
            
            # Create user
            user = self.user_repository.create_user(
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            
            return self.create_success_response(
                data={
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                message="User registered successfully"
            )
            
        except ValidationError as e:
            return self.handle_service_error(e, str(e))
        except Exception as e:
            return self.handle_service_error(e, "Failed to register user")
    
    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate a user with email and password.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            Dictionary with success status and user data or error message
        """
        try:
            # Validate email format
            if not self.validate_email_format(email):
                raise ValidationError("Invalid email format")
            
            # Authenticate user
            user = authenticate(username=email, password=password)
            
            if user is None:
                raise ValidationError("Invalid email or password")
            
            
            return self.create_success_response(
                data={
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                message="Authentication successful"
            )
            
        except ValidationError as e:
            return self.handle_service_error(e, str(e))
        except Exception as e:
            return self.handle_service_error(e, "Authentication failed")
