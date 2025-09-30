"""
Integration tests for UserService.
"""
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from src.core.services.user_service import UserService
from tests.factories import UserFactory

User = get_user_model()


@pytest.mark.integration
class TestUserServiceIntegration(TestCase):
    """Integration tests for UserService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = UserService()
    
    def test_register_user_integration(self):
        """Test user registration with real database."""
        # Arrange
        user_data = {
            'email': 'integration@example.com',
            'password': 'testpass123',
            'first_name': 'Integration',
            'last_name': 'Test'
        }
        
        # Act
        result = self.service.register_user(user_data)
        
        # Assert
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'User registered successfully')
        self.assertEqual(result['data']['email'], 'integration@example.com')
        
        # Verify user was created in database
        user = User.objects.get(email='integration@example.com')
        self.assertEqual(user.first_name, 'Integration')
        self.assertEqual(user.last_name, 'Test')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_register_user_duplicate_email(self):
        """Test user registration with duplicate email."""
        # Arrange
        UserFactory(email='duplicate@example.com')
        user_data = {
            'email': 'duplicate@example.com',
            'password': 'testpass123',
            'first_name': 'Duplicate',
            'last_name': 'User'
        }
        
        # Act
        result = self.service.register_user(user_data)
        
        # Assert
        self.assertFalse(result['success'])
        self.assertIn('User with this email already exists', result['message'])
    
    def test_authenticate_user_integration(self):
        """Test user authentication with real database."""
        # Arrange
        user = UserFactory(
            email='auth@example.com',
            first_name='Auth',
            last_name='User'
        )
        user.set_password('testpass123')
        user.save()
        
        # Act
        result = self.service.authenticate_user('auth@example.com', 'testpass123')
        
        # Assert
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Authentication successful')
        self.assertEqual(result['data']['email'], 'auth@example.com')
        self.assertEqual(result['data']['first_name'], 'Auth')
    
    def test_authenticate_user_invalid_credentials(self):
        """Test user authentication with invalid credentials."""
        # Arrange
        UserFactory(email='invalid@example.com')
        
        # Act
        result = self.service.authenticate_user('invalid@example.com', 'wrongpassword')
        
        # Assert
        self.assertFalse(result['success'])
        self.assertIn('Invalid email or password', result['message'])
    
    def test_validate_email_format(self):
        """Test email format validation."""
        # Test valid emails
        valid_emails = [
            'test@example.com',
            'user.name@domain.co.uk',
            'test+tag@example.org'
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(self.service.validate_email_format(email))
        
        # Test invalid emails
        invalid_emails = [
            'invalid-email',
            '@example.com',
            'test@',
            'test.example.com'
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(self.service.validate_email_format(email))
    
    def test_validate_password_strength(self):
        """Test password strength validation."""
        # Test valid passwords
        valid_passwords = [
            'password123',
            'strongpass',
            '12345678',
            'verylongpassword'
        ]
        
        for password in valid_passwords:
            with self.subTest(password=password):
                self.assertTrue(self.service.validate_password_strength(password))
        
        # Test invalid passwords
        invalid_passwords = [
            'short',
            '1234567',
            '',
            'abc'
        ]
        
        for password in invalid_passwords:
            with self.subTest(password=password):
                self.assertFalse(self.service.validate_password_strength(password))
