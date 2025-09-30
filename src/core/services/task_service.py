from typing import Dict, Any, List, Optional
from django.core.exceptions import ValidationError
from src.core.models import Task
from ..repositories.task_repository import TaskRepository
from .base_service import BaseService


class TaskService(BaseService):
    """
    Service class for task-related business logic.
    Handles task creation, status updates, and search operations.
    """
    
    def __init__(self):
        self.task_repository = TaskRepository()
    
    def create_task(self, user_id: int, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new task for a user.
        
        Args:
            user_id: ID of the user creating the task
            task_data: Dictionary containing task information (detail)
            
        Returns:
            Dictionary with success status and task data or error message
        """
        try:
            # Validate required fields
            required_fields = ['detail']
            self.validate_required_fields(task_data, required_fields)
            
            # Validate detail is not empty
            if not task_data['detail'].strip():
                raise ValidationError("Task detail cannot be empty")
            
            # Create task
            task = self.task_repository.create(
                detail=task_data['detail'].strip(),
                user_id=user_id,
                status='pending'
            )
            
            return self.create_success_response(
                data={
                    'id': task.id,
                    'detail': task.detail,
                    'status': task.status,
                    'created_at': task.created_at,
                    'updated_at': task.updated_at
                },
                message="Task created successfully"
            )
            
        except ValidationError as e:
            return self.handle_service_error(e, str(e))
        except Exception as e:
            return self.handle_service_error(e, "Error creating task")
    
    def update_task_status(self, user_id: int, task_id: int, new_status: str) -> Dict[str, Any]:
        """
        Update the status of a task.
        
        Args:
            user_id: ID of the user
            task_id: ID of the task to update
            new_status: New status for the task
            
        Returns:
            Dictionary with success status and updated task data or error message
        """
        try:
            # Validate status
            valid_statuses = ['pending', 'completed', 'cancelled']
            if new_status not in valid_statuses:
                raise ValidationError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            
            # Update task status
            task = self.task_repository.update_status(task_id, user_id, new_status)
            
            if task is None:
                raise ValidationError("Task not found or you don't have permission to modify it")
            
            return self.create_success_response(
                data={
                    'id': task.id,
                    'detail': task.detail,
                    'status': task.status,
                    'created_at': task.created_at,
                    'updated_at': task.updated_at
                },
                message="Task status updated successfully"
            )
            
        except ValidationError as e:
            return self.handle_service_error(e, str(e))
        except Exception as e:
            return self.handle_service_error(e, "Error updating task status")
    
    def search_tasks(self, user_id: int, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search tasks by detail and/or creation date.
        
        Args:
            user_id: ID of the user
            search_params: Dictionary containing search criteria (detail, created_date)
            
        Returns:
            Dictionary with success status and list of tasks or error message
        """
        try:
            detail = search_params.get('detail', '').strip()
            created_date = search_params.get('created_date')
            
            # If no search criteria provided, return all user tasks
            if not detail and not created_date:
                tasks = self.task_repository.get_by_user(user_id)
            # Search by both criteria
            elif detail and created_date:
                tasks = self.task_repository.search_by_detail_and_date(user_id, detail, created_date)
            # Search by detail only
            elif detail:
                tasks = self.task_repository.search_by_detail(user_id, detail)
            # Search by date only
            else:
                tasks = self.task_repository.search_by_created_date(user_id, created_date)
            
            # Convert tasks to dictionary format
            tasks_data = []
            for task in tasks:
                tasks_data.append({
                    'id': task.id,
                    'detail': task.detail,
                    'status': task.status,
                    'created_at': task.created_at,
                    'updated_at': task.updated_at
                })
            
            return self.create_success_response(
                data={
                    'tasks': tasks_data,
                    'total': len(tasks_data)
                },
                message="Search completed successfully"
            )
            
        except Exception as e:
            return self.handle_service_error(e, "Error searching tasks")
