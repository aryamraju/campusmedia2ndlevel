from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError
from .models import User, Announcement
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


@api_view(['POST'])
def create_announcement(request):
    """
    Create a new announcement
    POST /api/announcements/create/
    """
    title = request.data.get('title')
    content = request.data.get('content')
    created_by_id = request.data.get('created_by_id')
    target_role = request.data.get('target_role', None)
    
    if not title or not content or not created_by_id:
        return Response({
            'success': False,
            'message': 'Title, content, and created_by_id are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=created_by_id)
        if user.role not in ['Staff', 'Principal', 'Admin']:
            return Response({
                'success': False,
                'message': 'Only Staff, Principal, or Admin can create announcements'
            }, status=status.HTTP_403_FORBIDDEN)
        
        announcement = Announcement.objects.create(
            title=title,
            content=content,
            created_by=user,
            target_role=target_role
        )
        
        return Response({
            'success': True,
            'message': 'Announcement created successfully',
            'announcement': {
                'id': announcement.id,
                'title': announcement.title,
                'content': announcement.content,
                'created_by': announcement.created_by.get_full_name(),
                'created_at': announcement.created_at
            }
        }, status=status.HTTP_201_CREATED)
        
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error creating announcement: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_announcements(request):
    """
    Get all announcements
    GET /api/announcements/
    """
    announcements = Announcement.objects.filter(is_active=True).select_related('created_by')
    
    data = [{
        'id': ann.id,
        'title': ann.title,
        'content': ann.content,
        'created_by': ann.created_by.get_full_name(),
        'target_role': ann.target_role,
        'created_at': ann.created_at
    } for ann in announcements]
    
    return Response({
        'success': True,
        'count': len(data),
        'announcements': data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_staff_details(request):
    """
    Update staff professional details
    POST /api/users/update-staff-details/
    """
    user_id = request.data.get('user_id')
    qualification = request.data.get('qualification')
    subject_expertise = request.data.get('subject_expertise')
    assigned_classes = request.data.get('assigned_classes')
    experience_years = request.data.get('experience_years')
    
    if not user_id:
        return Response({
            'success': False,
            'message': 'User ID is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        
        # Verify user is staff
        if user.role not in ['Staff', 'Principal']:
            return Response({
                'success': False,
                'message': 'Only Staff and Principal can update staff details'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Update fields
        if qualification:
            user.qualification = qualification
        if subject_expertise:
            user.subject_expertise = subject_expertise
        if assigned_classes:
            user.assigned_classes = assigned_classes
        if experience_years is not None:
            user.experience_years = int(experience_years)
        
        user.save()
        
        return Response({
            'success': True,
            'message': 'Staff details updated successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'qualification': user.qualification,
                'subject_expertise': user.subject_expertise,
                'assigned_classes': user.assigned_classes,
                'experience_years': user.experience_years
            }
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({
            'success': False,
            'message': 'Invalid experience years value'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error updating staff details: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_student_details(request):
    """
    Update student academic details
    POST /api/users/update-student-details/
    """
    user_id = request.data.get('user_id')
    student_class = request.data.get('student_class')
    stream = request.data.get('stream')
    year = request.data.get('year')
    department = request.data.get('department')
    
    if not user_id:
        return Response({
            'success': False,
            'message': 'User ID is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        
        # Verify user is student
        if user.role != 'Student':
            return Response({
                'success': False,
                'message': 'Only Students can update student details'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Update fields
        if student_class:
            user.student_class = student_class
        if stream:
            user.stream = stream
        if year:
            user.year = year
        if department:
            user.department = department
        
        user.save()
        
        return Response({
            'success': True,
            'message': 'Student details updated successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'student_class': user.student_class,
                'stream': user.stream,
                'year': user.year,
                'department': user.department
            }
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error updating student details: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
