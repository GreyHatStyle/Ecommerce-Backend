from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length = 30,
        error_messages={
            'max_length' : 'username can not be more than 30 chars',
            'blank': 'username cannot be blank',
            'required': 'username is required'
        }
    )
    
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        error_messages={
            'min_length': 'Password must be at least 8 characters',
            'blank': 'Password cannot be blank',
            'required': 'Password is required'
        }
    )