"""
Unit tests for TaskService.
"""
import pytest
from unittest.mock import Mock, patch
from django.core.exceptions import ValidationError
from src.core.services.task_service import TaskService
from tests.factories import TaskFactory, UserFactory


@pytest.mark.unit
class TestTaskService:
    """Test cases for TaskService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Service will be created in each test after mocking
        pass
    
    def test_init(self):
        """Test service initialization."""
        service = TaskService()
        assert hasattr(service, 'task_repository')
    
    @patch('src.core.services.task_service.TaskService.validate_required_fields')
    @patch('src.core.services.task_service.TaskRepository')
    def test_create_task_success(self, mock_repo_class, mock_validate_required):
        """Test successful task creation."""
        # Arrange
        user_id = 1
        task_data = {'detail': 'Test task description'}
        mock_task = Mock()
        mock_task.id = 1
        mock_task.detail = 'Test task description'
        mock_task.status = 'pending'
        mock_task.created_at = '2025-09-30T10:00:00Z'
        mock_task.updated_at = '2025-09-30T10:00:00Z'
        
        # Configure mocks BEFORE creating service
        mock_repo = mock_repo_class.return_value
        mock_validate_required.return_value = None
        mock_repo.create.return_value = mock_task
        
        # Create service AFTER configuring mocks
        service = TaskService()
        
        # Act
        result = service.create_task(user_id, task_data)
        
        # Assert
        assert result['success'] is True
        assert result['message'] == 'Task created successfully'
        assert result['data']['id'] == 1
        assert result['data']['detail'] == 'Test task description'
        assert result['data']['status'] == 'pending'
        mock_repo.create.assert_called_once()
    
    @patch('src.core.services.task_service.TaskService.validate_required_fields')
    def test_create_task_missing_detail(self, mock_validate_required):
        """Test task creation with missing detail field."""
        # Arrange
        user_id = 1
        task_data = {}
        mock_validate_required.side_effect = ValidationError("Missing required fields")
        
        # Create service
        service = TaskService()
        
        # Act
        result = service.create_task(user_id, task_data)
        
        # Assert
        assert result['success'] is False
        assert 'Missing required fields' in result['message']
    
    @patch('src.core.services.task_service.TaskService.validate_required_fields')
    def test_create_task_empty_detail(self, mock_validate_required):
        """Test task creation with empty detail."""
        # Arrange
        user_id = 1
        task_data = {'detail': '   '}  # Empty/whitespace detail
        mock_validate_required.return_value = None
        
        # Create service
        service = TaskService()
        
        # Act
        result = service.create_task(user_id, task_data)
        
        # Assert
        assert result['success'] is False
        assert 'Task detail cannot be empty' in result['message']
    
    @patch('src.core.services.task_service.TaskRepository')
    def test_update_task_status_success(self, mock_repo_class):
        """Test successful task status update."""
        # Arrange
        user_id = 1
        task_id = 1
        new_status = 'completed'
        mock_task = Mock()
        mock_task.id = 1
        mock_task.detail = 'Test task'
        mock_task.status = 'completed'
        mock_task.created_at = '2025-09-30T10:00:00Z'
        mock_task.updated_at = '2025-09-30T10:01:00Z'
        
        # Configure mocks BEFORE creating service
        mock_repo = mock_repo_class.return_value
        mock_repo.update_status.return_value = mock_task
        
        # Create service AFTER configuring mocks
        service = TaskService()
        
        # Act
        result = service.update_task_status(user_id, task_id, new_status)
        
        # Assert
        assert result['success'] is True
        assert result['message'] == 'Task status updated successfully'
        assert result['data']['status'] == 'completed'
        mock_repo.update_status.assert_called_once_with(task_id, user_id, new_status)
    
    def test_update_task_status_invalid_status(self):
        """Test task status update with invalid status."""
        # Arrange
        user_id = 1
        task_id = 1
        new_status = 'invalid_status'
        
        # Create service
        service = TaskService()
        
        # Act
        result = service.update_task_status(user_id, task_id, new_status)
        
        # Assert
        assert result['success'] is False
        assert 'Invalid status' in result['message']
    
    @patch('src.core.services.task_service.TaskRepository')
    def test_update_task_status_not_found(self, mock_repo_class):
        """Test task status update when task not found."""
        # Arrange
        user_id = 1
        task_id = 999
        new_status = 'completed'
        
        # Configure mocks BEFORE creating service
        mock_repo = mock_repo_class.return_value
        mock_repo.update_status.return_value = None
        
        # Create service AFTER configuring mocks
        service = TaskService()
        
        # Act
        result = service.update_task_status(user_id, task_id, new_status)
        
        # Assert
        assert result['success'] is False
        assert 'Task not found or you don\'t have permission to modify it' in result['message']
    
    @patch('src.core.services.task_service.TaskRepository')
    def test_search_tasks_all(self, mock_repo_class):
        """Test searching all tasks."""
        # Arrange
        user_id = 1
        search_params = {}
        mock_tasks = [Mock(), Mock()]
        for i, task in enumerate(mock_tasks):
            task.id = i + 1
            task.detail = f'Task {i + 1}'
            task.status = 'pending'
            task.created_at = '2025-09-30T10:00:00Z'
            task.updated_at = '2025-09-30T10:00:00Z'
        
        # Configure mocks BEFORE creating service
        mock_repo = mock_repo_class.return_value
        mock_repo.get_by_user.return_value = mock_tasks
        
        # Create service AFTER configuring mocks
        service = TaskService()
        
        # Act
        result = service.search_tasks(user_id, search_params)
        
        # Assert
        assert result['success'] is True
        assert result['message'] == 'Search completed successfully'
        assert result['data']['total'] == 2
        assert len(result['data']['tasks']) == 2
        mock_repo.get_by_user.assert_called_once_with(user_id)
    
    @patch('src.core.services.task_service.TaskRepository')
    def test_search_tasks_by_detail(self, mock_repo_class):
        """Test searching tasks by detail."""
        # Arrange
        user_id = 1
        search_params = {'detail': 'test'}
        mock_tasks = [Mock()]
        mock_tasks[0].id = 1
        mock_tasks[0].detail = 'Test task'
        mock_tasks[0].status = 'pending'
        mock_tasks[0].created_at = '2025-09-30T10:00:00Z'
        mock_tasks[0].updated_at = '2025-09-30T10:00:00Z'
        
        # Configure mocks BEFORE creating service
        mock_repo = mock_repo_class.return_value
        mock_repo.search_by_detail.return_value = mock_tasks
        
        # Create service AFTER configuring mocks
        service = TaskService()
        
        # Act
        result = service.search_tasks(user_id, search_params)
        
        # Assert
        assert result['success'] is True
        assert result['data']['total'] == 1
        mock_repo.search_by_detail.assert_called_once_with(user_id, 'test')
    
    @patch('src.core.services.task_service.TaskRepository')
    def test_search_tasks_by_date(self, mock_repo_class):
        """Test searching tasks by created date."""
        # Arrange
        user_id = 1
        search_params = {'created_date': '2025-09-30'}
        mock_tasks = [Mock()]
        mock_tasks[0].id = 1
        mock_tasks[0].detail = 'Test task'
        mock_tasks[0].status = 'pending'
        mock_tasks[0].created_at = '2025-09-30T10:00:00Z'
        mock_tasks[0].updated_at = '2025-09-30T10:00:00Z'
        
        # Configure mocks BEFORE creating service
        mock_repo = mock_repo_class.return_value
        mock_repo.search_by_created_date.return_value = mock_tasks
        
        # Create service AFTER configuring mocks
        service = TaskService()
        
        # Act
        result = service.search_tasks(user_id, search_params)
        
        # Assert
        assert result['success'] is True
        assert result['data']['total'] == 1
        mock_repo.search_by_created_date.assert_called_once_with(user_id, '2025-09-30')
    
    @patch('src.core.services.task_service.TaskRepository')
    def test_search_tasks_by_detail_and_date(self, mock_repo_class):
        """Test searching tasks by both detail and date."""
        # Arrange
        user_id = 1
        search_params = {'detail': 'test', 'created_date': '2025-09-30'}
        mock_tasks = [Mock()]
        mock_tasks[0].id = 1
        mock_tasks[0].detail = 'Test task'
        mock_tasks[0].status = 'pending'
        mock_tasks[0].created_at = '2025-09-30T10:00:00Z'
        mock_tasks[0].updated_at = '2025-09-30T10:00:00Z'
        
        # Configure mocks BEFORE creating service
        mock_repo = mock_repo_class.return_value
        mock_repo.search_by_detail_and_date.return_value = mock_tasks
        
        # Create service AFTER configuring mocks
        service = TaskService()
        
        # Act
        result = service.search_tasks(user_id, search_params)
        
        # Assert
        assert result['success'] is True
        assert result['data']['total'] == 1
        mock_repo.search_by_detail_and_date.assert_called_once_with(user_id, 'test', '2025-09-30')
