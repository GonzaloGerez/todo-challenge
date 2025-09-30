"""
Integration tests for authentication API endpoints.
"""
import pytest
import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from tests.factories import UserFactory

User = get_user_model()


@pytest.mark.integration
class TestAuthEndpoints(TestCase):
    """Integration tests for authentication endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = Client()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
    
    def test_register_endpoint_success(self):
        """Test successful user registration via API."""
        # Arrange
        user_data = {
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        # Act
        response = self.client.post(
            self.register_url,
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'User registered successfully')
        self.assertEqual(data['data']['email'], 'newuser@example.com')
        self.assertEqual(data['data']['first_name'], 'New')
        self.assertEqual(data['data']['last_name'], 'User')
        
        # Verify user was created in database
        user = User.objects.get(email='newuser@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_register_endpoint_duplicate_email(self):
        """Test user registration with duplicate email via API."""
        # Arrange
        UserFactory(email='existing@example.com')
        user_data = {
            'email': 'existing@example.com',
            'password': 'testpass123',
            'first_name': 'Duplicate',
            'last_name': 'User'
        }
        
        # Act
        response = self.client.post(
            self.register_url,
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('User with this email already exists', data['message'])
    
    def test_register_endpoint_missing_fields(self):
        """Test user registration with missing required fields via API."""
        # Arrange
        user_data = {
            'email': 'incomplete@example.com',
            'password': 'testpass123'
            # Missing first_name and last_name
        }
        
        # Act
        response = self.client.post(
            self.register_url,
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Missing required fields', data['message'])
    
    def test_register_endpoint_invalid_email(self):
        """Test user registration with invalid email format via API."""
        # Arrange
        user_data = {
            'email': 'invalid-email',
            'password': 'testpass123',
            'first_name': 'Invalid',
            'last_name': 'Email'
        }
        
        # Act
        response = self.client.post(
            self.register_url,
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Invalid email format', data['message'])
    
    def test_login_endpoint_success(self):
        """Test successful user login via API."""
        # Arrange
        user = UserFactory(
            email='login@example.com',
            first_name='Login',
            last_name='User'
        )
        user.set_password('testpass123')
        user.save()
        
        login_data = {
            'email': 'login@example.com',
            'password': 'testpass123'
        }
        
        # Act
        response = self.client.post(
            self.login_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Authentication successful')
        self.assertEqual(data['data']['email'], 'login@example.com')
        self.assertEqual(data['data']['first_name'], 'Login')
        self.assertEqual(data['data']['last_name'], 'User')
        self.assertIn('access', data['data'])
        self.assertIn('refresh', data['data'])
        self.assertEqual(data['data']['expires_in'], 3600)
    
    def test_login_endpoint_invalid_credentials(self):
        """Test user login with invalid credentials via API."""
        # Arrange
        UserFactory(email='login@example.com')
        login_data = {
            'email': 'login@example.com',
            'password': 'wrongpassword'
        }
        
        # Act
        response = self.client.post(
            self.login_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Invalid email or password', data['message'])
    
    def test_login_endpoint_invalid_email(self):
        """Test user login with invalid email format via API."""
        # Arrange
        login_data = {
            'email': 'invalid-email',
            'password': 'testpass123'
        }
        
        # Act
        response = self.client.post(
            self.login_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Invalid email format', data['message'])
    
    def test_jwt_token_validation(self):
        """Test that JWT tokens are valid and can be used for authentication."""
        # Arrange
        user = UserFactory(email='jwt@example.com')
        user.set_password('testpass123')
        user.save()
        
        login_data = {
            'email': 'jwt@example.com',
            'password': 'testpass123'
        }
        
        # Act - Login to get token
        response = self.client.post(
            self.login_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        access_token = data['data']['access']
        
        # Test that token can be used for authenticated requests
        headers = {'Authorization': f'Bearer {access_token}'}
        health_response = self.client.get('/api/health/', **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        
        # Health endpoint should work with valid token
        self.assertEqual(health_response.status_code, status.HTTP_200_OK)
