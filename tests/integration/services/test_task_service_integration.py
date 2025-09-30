"""
Integration tests for TaskService.
"""
import pytest
from django.test import TestCase
from src.core.services.task_service import TaskService
from src.core.models import Task
from tests.factories import TaskFactory, UserFactory


@pytest.mark.integration
class TestTaskServiceIntegration(TestCase):
    """Integration tests for TaskService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = TaskService()
        self.user = UserFactory()
    
    def test_create_task_integration(self):
        """Test task creation with real database."""
        # Arrange
        task_data = {'detail': 'Integration test task'}
        
        # Act
        result = self.service.create_task(self.user.id, task_data)
        
        # Assert
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Task created successfully')
        self.assertEqual(result['data']['detail'], 'Integration test task')
        self.assertEqual(result['data']['status'], 'pending')
        
        # Verify task was created in database
        task = Task.objects.get(id=result['data']['id'])
        self.assertEqual(task.detail, 'Integration test task')
        self.assertEqual(task.status, 'pending')
        self.assertEqual(task.user, self.user)
    
    def test_create_task_empty_detail(self):
        """Test task creation with empty detail."""
        # Arrange
        task_data = {'detail': '   '}  # Empty/whitespace detail
        
        # Act
        result = self.service.create_task(self.user.id, task_data)
        
        # Assert
        self.assertFalse(result['success'])
        self.assertIn('Task detail cannot be empty', result['message'])
    
    def test_update_task_status_integration(self):
        """Test task status update with real database."""
        # Arrange
        task = TaskFactory(user=self.user, status='pending')
        
        # Act
        result = self.service.update_task_status(self.user.id, task.id, 'completed')
        
        # Assert
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Task status updated successfully')
        self.assertEqual(result['data']['status'], 'completed')
        
        # Verify task was updated in database
        task.refresh_from_db()
        self.assertEqual(task.status, 'completed')
    
    def test_update_task_status_not_found(self):
        """Test task status update with non-existent task."""
        # Arrange
        non_existent_task_id = 999
        
        # Act
        result = self.service.update_task_status(self.user.id, non_existent_task_id, 'completed')
        
        # Assert
        self.assertFalse(result['success'])
        self.assertIn('Task not found or you don\'t have permission to modify it', result['message'])
    
    def test_update_task_status_wrong_user(self):
        """Test task status update with task belonging to different user."""
        # Arrange
        other_user = UserFactory()
        task = TaskFactory(user=other_user, status='pending')
        
        # Act
        result = self.service.update_task_status(self.user.id, task.id, 'completed')
        
        # Assert
        self.assertFalse(result['success'])
        self.assertIn('Task not found or you don\'t have permission to modify it', result['message'])
    
    def test_search_tasks_all_integration(self):
        """Test searching all tasks with real database."""
        # Arrange
        task1 = TaskFactory(user=self.user, detail='First task')
        task2 = TaskFactory(user=self.user, detail='Second task')
        TaskFactory(user=UserFactory(), detail='Other user task')  # Different user
        
        # Act
        result = self.service.search_tasks(self.user.id, {})
        
        # Assert
        self.assertTrue(result['success'])
        self.assertEqual(result['data']['total'], 2)
        self.assertEqual(len(result['data']['tasks']), 2)
        
        # Verify only user's tasks are returned
        task_details = [task['detail'] for task in result['data']['tasks']]
        self.assertIn('First task', task_details)
        self.assertIn('Second task', task_details)
        self.assertNotIn('Other user task', task_details)
    
    def test_search_tasks_by_detail_integration(self):
        """Test searching tasks by detail with real database."""
        # Arrange
        task1 = TaskFactory(user=self.user, detail='Documentation task')
        task2 = TaskFactory(user=self.user, detail='Code review task')
        task3 = TaskFactory(user=self.user, detail='Testing task')
        
        # Act
        result = self.service.search_tasks(self.user.id, {'detail': 'task'})
        
        # Assert
        self.assertTrue(result['success'])
        self.assertEqual(result['data']['total'], 3)
        
        # Test more specific search
        result = self.service.search_tasks(self.user.id, {'detail': 'Documentation'})
        self.assertEqual(result['data']['total'], 1)
        self.assertEqual(result['data']['tasks'][0]['detail'], 'Documentation task')
    
    def test_search_tasks_by_date_integration(self):
        """Test searching tasks by created date with real database."""
        # Arrange
        from django.utils import timezone
        from datetime import date
        
        # Create tasks with specific dates
        task1 = TaskFactory(user=self.user, detail='Today task')
        task2 = TaskFactory(user=self.user, detail='Yesterday task')
        
        # Act
        today = date.today().strftime('%Y-%m-%d')
        result = self.service.search_tasks(self.user.id, {'created_date': today})
        
        # Assert
        self.assertTrue(result['success'])
        # At least one task should be found (the one created today)
        self.assertGreaterEqual(result['data']['total'], 1)
    
    def test_search_tasks_by_detail_and_date_integration(self):
        """Test searching tasks by both detail and date with real database."""
        # Arrange
        from datetime import date
        
        task1 = TaskFactory(user=self.user, detail='Documentation task')
        task2 = TaskFactory(user=self.user, detail='Code task')
        
        # Act
        today = date.today().strftime('%Y-%m-%d')
        result = self.service.search_tasks(self.user.id, {
            'detail': 'Documentation',
            'created_date': today
        })
        
        # Assert
        self.assertTrue(result['success'])
        self.assertEqual(result['data']['total'], 1)
        self.assertEqual(result['data']['tasks'][0]['detail'], 'Documentation task')
    
    def test_task_status_choices(self):
        """Test that only valid status values are accepted."""
        # Arrange
        task = TaskFactory(user=self.user, status='pending')
        
        # Test valid statuses
        valid_statuses = ['pending', 'completed', 'cancelled']
        for status in valid_statuses:
            with self.subTest(status=status):
                result = self.service.update_task_status(self.user.id, task.id, status)
                self.assertTrue(result['success'])
        
        # Test invalid status
        result = self.service.update_task_status(self.user.id, task.id, 'invalid_status')
        self.assertFalse(result['success'])
        self.assertIn('Invalid status', result['message'])
