from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User=get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['id','email', 'password', 'first_name', 'last_name','phone_number', 'house_number', 'confirm_password']
        extra_kwargs={'password':{'write_only':True}}
        
        def validate(self, attrs):
            if attrs['password'] != attrs['confirm_password']:
                raise serializers.ValidationError(
                    {"confirm_password":"passwords do not match"}
                )
                
            return attrs
        
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user=User.objects.create_user(**validated_data)
        return user
    
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'email', 'first_name', 'last_name', 'phone_number', 'house_number']
    
