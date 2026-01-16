from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError
from .models import User
from .serializers import UserSerializer, UserLoginSerializer, UserResponseSerializer


@api_view(['POST'])
def register_user(request):
    """
    Register a new user
    POST /api/users/register/
    """
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            user = serializer.save()
            response_serializer = UserResponseSerializer(user)
            return Response({
                'success': True,
                'message': 'User registered successfully',
                'user': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            if 'email' in str(e):
                return Response({
                    'success': False,
                    'message': 'Email already registered'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif 'register_number' in str(e):
                return Response({
                    'success': False,
                    'message': 'Register number already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'message': 'Registration failed'
                }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'success': False,
        'message': 'Invalid data',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    """
    Login user
    POST /api/users/login/
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        response_serializer = UserResponseSerializer(user)
        return Response({
            'success': True,
            'message': 'Login successful',
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Invalid credentials',
        'errors': serializer.errors
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_all_users(request):
    """
    Get all users (for testing/admin purposes)
    GET /api/users/
    """
    users = User.objects.all()
    serializer = UserResponseSerializer(users, many=True)
    return Response({
        'success': True,
        'count': users.count(),
        'users': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user(request, user_id):
    """
    Get a specific user by ID
    GET /api/users/<id>/
    """
    try:
        user = User.objects.get(id=user_id)
        serializer = UserResponseSerializer(user)
        return Response({
            'success': True,
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
