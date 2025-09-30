"""
Unit tests for TaskRepository.
"""
import pytest
from unittest.mock import Mock, patch
from src.core.repositories.task_repository import TaskRepository
from src.core.models import Task
from tests.factories import TaskFactory, UserFactory


@pytest.mark.unit
class TestTaskRepository:
    """Test cases for TaskRepository."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.repository = TaskRepository()
    
    def test_init(self):
        """Test repository initialization."""
        assert self.repository.model == Task
    
    @patch('src.core.repositories.task_repository.Task.objects')
    def test_get_by_user(self, mock_objects):
        """Test getting tasks by user."""
        # Arrange
        user_id = 1
        mock_tasks = [Mock(), Mock()]
        mock_objects.filter.return_value = mock_tasks
        
        # Act
        result = self.repository.get_by_user(user_id)
        
        # Assert
        mock_objects.filter.assert_called_once_with(user_id=user_id)
        assert result == mock_tasks
    
    @patch('src.core.repositories.task_repository.Task.objects')
    def test_get_by_user_and_status(self, mock_objects):
        """Test getting tasks by user and status."""
        # Arrange
        user_id = 1
        status = "pending"
        mock_tasks = [Mock()]
        mock_objects.filter.return_value = mock_tasks
        
        # Act
        result = self.repository.get_by_user_and_status(user_id, status)
        
        # Assert
        mock_objects.filter.assert_called_once_with(user_id=user_id, status=status)
        assert result == mock_tasks
    
    @patch('src.core.repositories.task_repository.Task.objects')
    def test_search_by_detail(self, mock_objects):
        """Test searching tasks by detail."""
        # Arrange
        user_id = 1
        detail = "test task"
        mock_tasks = [Mock(), Mock()]
        mock_objects.filter.return_value.order_by.return_value = mock_tasks
        
        # Act
        result = self.repository.search_by_detail(user_id, detail)
        
        # Assert
        mock_objects.filter.assert_called_once_with(
            user_id=user_id,
            detail__icontains=detail
        )
        mock_objects.filter.return_value.order_by.assert_called_once_with('-created_at')
        assert result == mock_tasks
    
    @patch('src.core.repositories.task_repository.Task.objects')
    def test_search_by_created_date(self, mock_objects):
        """Test searching tasks by created date."""
        # Arrange
        user_id = 1
        date = "2025-09-30"
        mock_tasks = [Mock()]
        mock_objects.filter.return_value.order_by.return_value = mock_tasks
        
        # Act
        result = self.repository.search_by_created_date(user_id, date)
        
        # Assert
        mock_objects.filter.assert_called_once_with(
            user_id=user_id,
            created_at__date=date
        )
        mock_objects.filter.return_value.order_by.assert_called_once_with('-created_at')
        assert result == mock_tasks
    
    @patch('src.core.repositories.task_repository.Task.objects')
    def test_search_by_detail_and_date(self, mock_objects):
        """Test searching tasks by detail and date."""
        # Arrange
        user_id = 1
        detail = "test task"
        date = "2025-09-30"
        mock_tasks = [Mock()]
        mock_objects.filter.return_value.order_by.return_value = mock_tasks
        
        # Act
        result = self.repository.search_by_detail_and_date(user_id, detail, date)
        
        # Assert
        mock_objects.filter.assert_called_once_with(
            user_id=user_id,
            detail__icontains=detail,
            created_at__date=date
        )
        mock_objects.filter.return_value.order_by.assert_called_once_with('-created_at')
        assert result == mock_tasks
    
    @patch('src.core.repositories.task_repository.Task.objects')
    def test_update_status_success(self, mock_objects):
        """Test updating task status successfully."""
        # Arrange
        task_id = 1
        user_id = 1
        new_status = "completed"
        mock_task = Mock()
        mock_objects.get.return_value = mock_task
        
        # Act
        result = self.repository.update_status(task_id, user_id, new_status)
        
        # Assert
        mock_objects.get.assert_called_once_with(id=task_id, user_id=user_id)
        assert mock_task.status == new_status
        mock_task.save.assert_called_once()
        assert result == mock_task
    
    @patch('src.core.repositories.task_repository.Task.objects')
    def test_update_status_not_found(self, mock_objects):
        """Test updating task status when task not found."""
        # Arrange
        task_id = 999
        user_id = 1
        new_status = "completed"
        mock_objects.get.side_effect = Task.DoesNotExist()
        
        # Act
        result = self.repository.update_status(task_id, user_id, new_status)
        
        # Assert
        assert result is None
    
    @patch('src.core.repositories.task_repository.Task.objects')
    def test_get_by_id_and_user(self, mock_objects):
        """Test getting task by ID and user."""
        # Arrange
        task_id = 1
        user_id = 1
        mock_task = Mock()
        mock_objects.filter.return_value.first.return_value = mock_task
        
        # Act
        result = self.repository.get_by_id_and_user(task_id, user_id)
        
        # Assert
        mock_objects.filter.assert_called_once_with(id=task_id, user_id=user_id)
        assert result == mock_task
