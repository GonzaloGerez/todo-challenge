"""
Unit tests for UserRepository.
"""
import pytest
from unittest.mock import Mock, patch
from src.core.repositories.user_repository import UserRepository
from src.authentication.models import User
from tests.factories import UserFactory


@pytest.mark.unit
class TestUserRepository:
    """Test cases for UserRepository."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.repository = UserRepository()
    
    def test_init(self):
        """Test repository initialization."""
        assert self.repository.model == User
    
    @patch('src.core.repositories.user_repository.User.objects')
    def test_get_by_email(self, mock_objects):
        """Test getting user by email."""
        # Arrange
        email = "test@example.com"
        mock_user = Mock()
        mock_objects.filter.return_value.first.return_value = mock_user
        
        # Act
        result = self.repository.get_by_email(email)
        
        # Assert
        mock_objects.filter.assert_called_once_with(email=email)
        assert result == mock_user
    
    @patch('src.core.repositories.user_repository.User.objects')
    def test_get_by_email_not_found(self, mock_objects):
        """Test getting user by email when not found."""
        # Arrange
        email = "nonexistent@example.com"
        mock_objects.filter.return_value.first.return_value = None
        
        # Act
        result = self.repository.get_by_email(email)
        
        # Assert
        assert result is None
    
    @patch('src.core.repositories.user_repository.User.objects')
    def test_create_user(self, mock_objects):
        """Test creating a new user."""
        # Arrange
        email = "newuser@example.com"
        password = "testpass123"
        first_name = "John"
        last_name = "Doe"
        mock_user = Mock()
        mock_objects.create.return_value = mock_user
        
        # Act
        result = self.repository.create_user(email, password, first_name, last_name)
        
        # Assert
        mock_objects.create.assert_called_once()
        call_args = mock_objects.create.call_args
        assert call_args[1]['email'] == email
        assert call_args[1]['first_name'] == first_name
        assert call_args[1]['last_name'] == last_name
        assert 'password' in call_args[1]  # Password should be hashed
        assert result == mock_user
    
    @patch('src.core.repositories.user_repository.User.objects')
    def test_email_exists_true(self, mock_objects):
        """Test email exists when user exists."""
        # Arrange
        email = "existing@example.com"
        mock_objects.filter.return_value.exists.return_value = True
        
        # Act
        result = self.repository.email_exists(email)
        
        # Assert
        mock_objects.filter.assert_called_once_with(email=email)
        assert result is True
    
    @patch('src.core.repositories.user_repository.User.objects')
    def test_email_exists_false(self, mock_objects):
        """Test email exists when user doesn't exist."""
        # Arrange
        email = "nonexistent@example.com"
        mock_objects.filter.return_value.exists.return_value = False
        
        # Act
        result = self.repository.email_exists(email)
        
        # Assert
        mock_objects.filter.assert_called_once_with(email=email)
        assert result is False
