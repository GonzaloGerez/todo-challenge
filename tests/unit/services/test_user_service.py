"""
Unit tests for UserService.
"""
import pytest
from unittest.mock import Mock, patch
from django.core.exceptions import ValidationError
from src.core.services.user_service import UserService
from tests.factories import UserFactory


@pytest.mark.unit
class TestUserService:
    """Test cases for UserService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Service will be created in each test after mocking
        pass
    
    def test_init(self):
        """Test service initialization."""
        service = UserService()
        assert hasattr(service, 'user_repository')
    
    @patch('src.core.services.user_service.UserService.validate_required_fields')
    @patch('src.core.services.user_service.UserService.validate_email_format')
    @patch('src.core.services.user_service.UserService.validate_password_strength')
    @patch('src.core.services.user_service.UserRepository')
    def test_register_user_success(self, mock_repo_class, mock_validate_password, 
                                 mock_validate_email, mock_validate_required):
        """Test successful user registration."""
        # Arrange
        user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        mock_user = Mock()
        mock_user.id = 1
        mock_user.email = 'test@example.com'
        mock_user.first_name = 'John'
        mock_user.last_name = 'Doe'
        
        # Configure mocks BEFORE creating service
        mock_repo = mock_repo_class.return_value
        mock_validate_required.return_value = None
        mock_validate_email.return_value = True
        mock_validate_password.return_value = True
        mock_repo.email_exists.return_value = False
        mock_repo.create_user.return_value = mock_user
        
        # Create service AFTER configuring mocks
        service = UserService()
        
        # Act
        result = service.register_user(user_data)
        
        # Assert
        assert result['success'] is True
        assert result['message'] == 'User registered successfully'
        assert result['data']['id'] == 1
        assert result['data']['email'] == 'test@example.com'
        mock_repo.email_exists.assert_called_once_with('test@example.com')
        mock_repo.create_user.assert_called_once()
    
    @patch('src.core.services.user_service.UserService.validate_required_fields')
    def test_register_user_missing_fields(self, mock_validate_required):
        """Test user registration with missing required fields."""
        # Arrange
        user_data = {'email': 'test@example.com'}
        mock_validate_required.side_effect = ValidationError("Missing required fields")
        
        # Create service
        service = UserService()
        
        # Act
        result = service.register_user(user_data)
        
        # Assert
        assert result['success'] is False
        assert 'Missing required fields' in result['message']
    
    @patch('src.core.services.user_service.UserService.validate_required_fields')
    @patch('src.core.services.user_service.UserService.validate_email_format')
    def test_register_user_invalid_email(self, mock_validate_email, mock_validate_required):
        """Test user registration with invalid email."""
        # Arrange
        user_data = {
            'email': 'invalid-email',
            'password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        mock_validate_required.return_value = None
        mock_validate_email.return_value = False
        
        # Create service
        service = UserService()
        
        # Act
        result = service.register_user(user_data)
        
        # Assert
        assert result['success'] is False
        assert 'Invalid email format' in result['message']
    
    @patch('src.core.services.user_service.UserService.validate_required_fields')
    @patch('src.core.services.user_service.UserService.validate_email_format')
    @patch('src.core.services.user_service.UserService.validate_password_strength')
    @patch('src.core.services.user_service.UserRepository')
    def test_register_user_email_exists(self, mock_repo_class, mock_validate_password,
                                      mock_validate_email, mock_validate_required):
        """Test user registration when email already exists."""
        # Arrange
        user_data = {
            'email': 'existing@example.com',
            'password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        
        # Configure mocks BEFORE creating service
        mock_repo = mock_repo_class.return_value
        mock_validate_required.return_value = None
        mock_validate_email.return_value = True
        mock_validate_password.return_value = True
        mock_repo.email_exists.return_value = True
        
        # Create service AFTER configuring mocks
        service = UserService()
        
        # Act
        result = service.register_user(user_data)
        
        # Assert
        assert result['success'] is False
        assert 'User with this email already exists' in result['message']
    
    @patch('src.core.services.user_service.UserService.validate_email_format')
    @patch('src.core.services.user_service.authenticate')
    def test_authenticate_user_success(self, mock_authenticate, mock_validate_email):
        """Test successful user authentication."""
        # Arrange
        email = 'test@example.com'
        password = 'testpass123'
        mock_user = Mock()
        mock_user.id = 1
        mock_user.email = 'test@example.com'
        mock_user.first_name = 'John'
        mock_user.last_name = 'Doe'
        
        mock_validate_email.return_value = True
        mock_authenticate.return_value = mock_user
        
        # Create service
        service = UserService()
        
        # Act
        result = service.authenticate_user(email, password)
        
        # Assert
        assert result['success'] is True
        assert result['message'] == 'Authentication successful'
        assert result['data']['id'] == 1
        assert result['data']['email'] == 'test@example.com'
        mock_authenticate.assert_called_once_with(username=email, password=password)
    
    @patch('src.core.services.user_service.UserService.validate_email_format')
    def test_authenticate_user_invalid_email(self, mock_validate_email):
        """Test authentication with invalid email format."""
        # Arrange
        email = 'invalid-email'
        password = 'testpass123'
        mock_validate_email.return_value = False
        
        # Create service
        service = UserService()
        
        # Act
        result = service.authenticate_user(email, password)
        
        # Assert
        assert result['success'] is False
        assert 'Invalid email format' in result['message']
    
    @patch('src.core.services.user_service.UserService.validate_email_format')
    @patch('src.core.services.user_service.authenticate')
    def test_authenticate_user_invalid_credentials(self, mock_authenticate, mock_validate_email):
        """Test authentication with invalid credentials."""
        # Arrange
        email = 'test@example.com'
        password = 'wrongpassword'
        mock_validate_email.return_value = True
        mock_authenticate.return_value = None
        
        # Create service
        service = UserService()
        
        # Act
        result = service.authenticate_user(email, password)
        
        # Assert
        assert result['success'] is False
        assert 'Invalid email or password' in result['message']
