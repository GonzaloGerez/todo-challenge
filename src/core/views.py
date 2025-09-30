from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from src.core.services.task_service import TaskService


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint to verify API is running.
    """
    return Response({
        'status': 'healthy',
        'message': 'Todo API is running successfully',
        'version': '1.0.0'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    """
    Create a new task.
    
    Expected payload:
    {
        "detail": "Task description"
    }
    """
    task_service = TaskService()
    result = task_service.create_task(request.user.id, request.data)
    
    if result['success']:
        return Response(result, status=status.HTTP_201_CREATED)
    else:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task_status(request, task_id):
    """
    Update task status.
    
    Expected payload:
    {
        "status": "pending" | "completed" | "cancelled"
    }
    """
    task_service = TaskService()
    new_status = request.data.get('status')
    
    if not new_status:
        return Response({
            'success': False,
            'message': 'Status field is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    result = task_service.update_task_status(request.user.id, task_id, new_status)
    
    if result['success']:
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_tasks(request):
    """
    Search tasks by detail and/or creation date.
    
    Query parameters:
    - detail: Search in task description (optional)
    - created_date: Search by creation date in format YYYY-MM-DD (optional)
    """
    task_service = TaskService()
    
    # Get query parameters
    search_params = {
        'detail': request.GET.get('detail', ''),
        'created_date': request.GET.get('created_date')
    }
    
    result = task_service.search_tasks(request.user.id, search_params)
    
    if result['success']:
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)