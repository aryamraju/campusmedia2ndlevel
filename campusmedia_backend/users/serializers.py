from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'register_number', 
                  'phone', 'role', 'password', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},  # Don't return password in responses
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
    
    def create(self, validated_data):
        """Create a new user with encrypted password"""
        user = User.objects.create(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    
    def validate(self, data):
        """Validate login credentials"""
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        
        try:
            user = User.objects.get(email=email, role=role)
            if not user.check_password(password):
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')
        
        return data


class UserResponseSerializer(serializers.ModelSerializer):
    """Serializer for user response (without password)"""
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'register_number', 
                  'phone', 'role', 'is_active', 'profile_completed', 'created_at', 'updated_at']
