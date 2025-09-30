from typing import List, Optional
from django.db.models import Q
from src.core.models import Task
from .base_repository import BaseRepository


class TaskRepository(BaseRepository):
    """
    Repository for Task model operations.
    Handles all database operations related to tasks.
    """
    
    def __init__(self):
        super().__init__(Task)
    
    def get_by_user(self, user_id: int) -> List[Task]:
        """Get all tasks for a specific user."""
        return self.filter(user_id=user_id)
    
    def get_by_user_and_status(self, user_id: int, status: str) -> List[Task]:
        """Get tasks for a user filtered by status."""
        return self.filter(user_id=user_id, status=status)
    
    def search_by_detail(self, user_id: int, detail: str) -> List[Task]:
        """Search tasks by detail (case insensitive)."""
        return list(
            self.model.objects.filter(
                user_id=user_id,
                detail__icontains=detail
            ).order_by('-created_at')
        )
    
    def search_by_created_date(self, user_id: int, date) -> List[Task]:
        """Search tasks by creation date."""
        return list(
            self.model.objects.filter(
                user_id=user_id,
                created_at__date=date
            ).order_by('-created_at')
        )
    
    def search_by_detail_and_date(self, user_id: int, detail: str, date) -> List[Task]:
        """Search tasks by both detail and creation date."""
        return list(
            self.model.objects.filter(
                user_id=user_id,
                detail__icontains=detail,
                created_at__date=date
            ).order_by('-created_at')
        )
    
    def update_status(self, task_id: int, user_id: int, new_status: str) -> Optional[Task]:
        """Update only the status of a task."""
        try:
            task = self.model.objects.get(id=task_id, user_id=user_id)
            task.status = new_status
            task.save()
            return task
        except self.model.DoesNotExist:
            return None
    
    def get_by_id_and_user(self, task_id: int, user_id: int) -> Optional[Task]:
        """Get a task by ID ensuring it belongs to the user."""
        return self.get_first(id=task_id, user_id=user_id)
