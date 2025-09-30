from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    Custom middleware to handle exceptions and return JSON responses.
    """
    
    def process_exception(self, request, exception):
        """
        Process exceptions and return JSON error response.
        """
        logger.error(f"Exception occurred: {str(exception)}", exc_info=True)
        
        return JsonResponse({
            'success': False,
            'message': 'An internal server error occurred',
            'error': str(exception) if request.settings.DEBUG else 'Internal server error'
        }, status=500)

