from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from src.core.services.user_service import UserService


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user.
    
    Expected payload:
    {
        "email": "user@example.com",
        "password": "securepassword",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    user_service = UserService()
    result = user_service.register_user(request.data)
    
    if result['success']:
        return Response(result, status=status.HTTP_201_CREATED)
    else:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authenticate a user and return a JWT token.
    
    Expected payload:
    {
        "email": "user@example.com",
        "password": "securepassword"
    }
    """
    user_service = UserService()
    result = user_service.authenticate_user(
        email=request.data.get('email'),
        password=request.data.get('password')
    )
    
    if result['success']:
        # Get user and create JWT tokens
        from src.authentication.models import User
        user = User.objects.get(email=request.data.get('email'))
        
        # Create JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # Set token expiration to 1 hour
        access_token.set_exp(lifetime=timedelta(hours=1))
        
        result['data']['access'] = str(access_token)
        result['data']['refresh'] = str(refresh)
        result['data']['expires_in'] = 3600  # 1 hour in seconds
        
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(result, status=status.HTTP_401_UNAUTHORIZED)

