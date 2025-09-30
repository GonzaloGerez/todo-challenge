from abc import ABC, abstractmethod
from typing import List, Optional, Type, TypeVar
from django.db import models

T = TypeVar('T', bound=models.Model)


class BaseRepository(ABC):
    """
    Base repository class that defines the interface for all repositories.
    Implements common CRUD operations.
    """
    
    def __init__(self, model: Type[T]):
        self.model = model
    
    def create(self, **kwargs) -> T:
        """Create a new instance of the model."""
        return self.model.objects.create(**kwargs)
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Get an instance by its ID."""
        try:
            return self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return None
    
    def get_all(self) -> List[T]:
        """Get all instances of the model."""
        return list(self.model.objects.all())
    
    def filter(self, **kwargs) -> List[T]:
        """Filter instances based on given criteria."""
        return list(self.model.objects.filter(**kwargs))
    
    def get_first(self, **kwargs) -> Optional[T]:
        """Get the first instance matching the criteria."""
        try:
            return self.model.objects.filter(**kwargs).first()
        except self.model.DoesNotExist:
            return None
    
    def update(self, instance: T, **kwargs) -> T:
        """Update an existing instance."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    def delete(self, instance: T) -> bool:
        """Delete an instance."""
        try:
            instance.delete()
            return True
        except Exception:
            return False
    
    def exists(self, **kwargs) -> bool:
        """Check if an instance exists with the given criteria."""
        return self.model.objects.filter(**kwargs).exists()
    
    def count(self, **kwargs) -> int:
        """Count instances matching the criteria."""
        return self.model.objects.filter(**kwargs).count()

