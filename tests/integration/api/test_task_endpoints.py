"""
Integration tests for task API endpoints.
"""
import pytest
import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from src.core.models import Task
from tests.factories import UserFactory, TaskFactory

User = get_user_model()


@pytest.mark.integration
class TestTaskEndpoints(TestCase):
    """Integration tests for task endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = Client()
        self.user = UserFactory()
        self.other_user = UserFactory()
        
        # Create JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        
        self.create_url = '/api/tasks/'
        self.update_status_url = '/api/tasks/{}/status/'
        self.search_url = '/api/tasks/search/'
    
    def test_create_task_endpoint_success(self):
        """Test successful task creation via API."""
        # Arrange
        task_data = {'detail': 'API test task'}
        
        # Act
        response = self.client.post(
            self.create_url,
            data=json.dumps(task_data),
            content_type='application/json',
            **self.auth_headers
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Task created successfully')
        self.assertEqual(data['data']['detail'], 'API test task')
        self.assertEqual(data['data']['status'], 'pending')
        
        # Verify task was created in database
        task = Task.objects.get(id=data['data']['id'])
        self.assertEqual(task.detail, 'API test task')
        self.assertEqual(task.user, self.user)
    
    def test_create_task_endpoint_unauthorized(self):
        """Test task creation without authentication."""
        # Arrange
        task_data = {'detail': 'Unauthorized task'}
        
        # Act
        response = self.client.post(
            self.create_url,
            data=json.dumps(task_data),
            content_type='application/json'
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_task_endpoint_missing_detail(self):
        """Test task creation with missing detail field."""
        # Arrange
        task_data = {}
        
        # Act
        response = self.client.post(
            self.create_url,
            data=json.dumps(task_data),
            content_type='application/json',
            **self.auth_headers
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Missing required fields', data['message'])
    
    def test_create_task_endpoint_empty_detail(self):
        """Test task creation with empty detail."""
        # Arrange
        task_data = {'detail': '   '}  # Empty/whitespace detail
        
        # Act
        response = self.client.post(
            self.create_url,
            data=json.dumps(task_data),
            content_type='application/json',
            **self.auth_headers
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Task detail cannot be empty', data['message'])
    
    def test_update_task_status_endpoint_success(self):
        """Test successful task status update via API."""
        # Arrange
        task = TaskFactory(user=self.user, status='pending')
        update_data = {'status': 'completed'}
        
        # Act
        response = self.client.put(
            self.update_status_url.format(task.id),
            data=json.dumps(update_data),
            content_type='application/json',
            **self.auth_headers
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Task status updated successfully')
        self.assertEqual(data['data']['status'], 'completed')
        
        # Verify task was updated in database
        task.refresh_from_db()
        self.assertEqual(task.status, 'completed')
    
    def test_update_task_status_endpoint_unauthorized(self):
        """Test task status update without authentication."""
        # Arrange
        task = TaskFactory(user=self.user, status='pending')
        update_data = {'status': 'completed'}
        
        # Act
        response = self.client.put(
            self.update_status_url.format(task.id),
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_task_status_endpoint_not_found(self):
        """Test task status update with non-existent task."""
        # Arrange
        non_existent_task_id = 999
        update_data = {'status': 'completed'}
        
        # Act
        response = self.client.put(
            self.update_status_url.format(non_existent_task_id),
            data=json.dumps(update_data),
            content_type='application/json',
            **self.auth_headers
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Task not found or you don\'t have permission to modify it', data['message'])
    
    def test_update_task_status_endpoint_wrong_user(self):
        """Test task status update with task belonging to different user."""
        # Arrange
        task = TaskFactory(user=self.other_user, status='pending')
        update_data = {'status': 'completed'}
        
        # Act
        response = self.client.put(
            self.update_status_url.format(task.id),
            data=json.dumps(update_data),
            content_type='application/json',
            **self.auth_headers
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Task not found or you don\'t have permission to modify it', data['message'])
    
    def test_update_task_status_endpoint_invalid_status(self):
        """Test task status update with invalid status."""
        # Arrange
        task = TaskFactory(user=self.user, status='pending')
        update_data = {'status': 'invalid_status'}
        
        # Act
        response = self.client.put(
            self.update_status_url.format(task.id),
            data=json.dumps(update_data),
            content_type='application/json',
            **self.auth_headers
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Invalid status', data['message'])
    
    def test_update_task_status_endpoint_missing_status(self):
        """Test task status update with missing status field."""
        # Arrange
        task = TaskFactory(user=self.user, status='pending')
        update_data = {}
        
        # Act
        response = self.client.put(
            self.update_status_url.format(task.id),
            data=json.dumps(update_data),
            content_type='application/json',
            **self.auth_headers
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Status field is required', data['message'])
    
    def test_search_tasks_endpoint_all(self):
        """Test searching all tasks via API."""
        # Arrange
        task1 = TaskFactory(user=self.user, detail='First task')
        task2 = TaskFactory(user=self.user, detail='Second task')
        TaskFactory(user=self.other_user, detail='Other user task')  # Different user
        
        # Act
        response = self.client.get(self.search_url, **self.auth_headers)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Search completed successfully')
        self.assertEqual(data['data']['total'], 2)
        self.assertEqual(len(data['data']['tasks']), 2)
        
        # Verify only user's tasks are returned
        task_details = [task['detail'] for task in data['data']['tasks']]
        self.assertIn('First task', task_details)
        self.assertIn('Second task', task_details)
        self.assertNotIn('Other user task', task_details)
    
    def test_search_tasks_endpoint_unauthorized(self):
        """Test task search without authentication."""
        # Act
        response = self.client.get(self.search_url)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_search_tasks_endpoint_by_detail(self):
        """Test searching tasks by detail via API."""
        # Arrange
        task1 = TaskFactory(user=self.user, detail='Documentation task')
        task2 = TaskFactory(user=self.user, detail='Code review task')
        task3 = TaskFactory(user=self.user, detail='Testing task')
        
        # Act
        response = self.client.get(
            f'{self.search_url}?detail=task',
            **self.auth_headers
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['total'], 3)
        
        # Test more specific search
        response = self.client.get(
            f'{self.search_url}?detail=Documentation',
            **self.auth_headers
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['total'], 1)
        self.assertEqual(data['data']['tasks'][0]['detail'], 'Documentation task')
    
    def test_search_tasks_endpoint_by_date(self):
        """Test searching tasks by created date via API."""
        # Arrange
        from datetime import date
        task1 = TaskFactory(user=self.user, detail='Today task')
        task2 = TaskFactory(user=self.user, detail='Yesterday task')
        
        # Act
        today = date.today().strftime('%Y-%m-%d')
        response = self.client.get(
            f'{self.search_url}?created_date={today}',
            **self.auth_headers
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(data['data']['total'], 1)
    
    def test_search_tasks_endpoint_by_detail_and_date(self):
        """Test searching tasks by both detail and date via API."""
        # Arrange
        from datetime import date
        task1 = TaskFactory(user=self.user, detail='Documentation task')
        task2 = TaskFactory(user=self.user, detail='Code task')
        
        # Act
        today = date.today().strftime('%Y-%m-%d')
        response = self.client.get(
            f'{self.search_url}?detail=Documentation&created_date={today}',
            **self.auth_headers
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['total'], 1)
        self.assertEqual(data['data']['tasks'][0]['detail'], 'Documentation task')
    
    def test_task_status_choices_api(self):
        """Test that only valid status values are accepted via API."""
        # Arrange
        task = TaskFactory(user=self.user, status='pending')
        
        # Test valid statuses
        valid_statuses = ['pending', 'completed', 'cancelled']
        for status_value in valid_statuses:
            with self.subTest(status=status_value):
                response = self.client.put(
                    self.update_status_url.format(task.id),
                    data=json.dumps({'status': status_value}),
                    content_type='application/json',
                    **self.auth_headers
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test invalid status
        response = self.client.put(
            self.update_status_url.format(task.id),
            data=json.dumps({'status': 'invalid_status'}),
            content_type='application/json',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
