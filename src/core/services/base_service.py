from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from django.core.exceptions import ValidationError


class BaseService(ABC):
    """
    Base service class that defines the interface for all business logic services.
    Contains common validation and error handling methods.
    """
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> None:
        """Validate that all required fields are present in the data."""
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    
    def validate_email_format(self, email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_password_strength(self, password: str) -> bool:
        """Validate password strength."""
        if len(password) < 8:
            return False
        # Add more password validation rules as needed
        return True
    
    def handle_service_error(self, error: Exception, message: str = "An error occurred") -> Dict[str, Any]:
        """Handle service errors and return standardized error response."""
        return {
            'success': False,
            'message': message,
            'error': str(error)
        }
    
    def create_success_response(self, data: Any = None, message: str = "Operation successful") -> Dict[str, Any]:
        """Create standardized success response."""
        response = {
            'success': True,
            'message': message
        }
        if data is not None:
            response['data'] = data
        return response

