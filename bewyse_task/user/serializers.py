from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserProfileSerializer(serializers.Serializer):  
    username = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class RegisterSerializer(serializers.ModelSerializer):   
    email = serializers.EmailField(required =True)
    username = serializers.CharField(required =False)
    password = serializers.CharField(required = True, write_only = True, validators = [validate_password])
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ["email","username", "first_name", "last_name", "password"]
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required =True, max_length=100)
    password = serializers.CharField(required = True, write_only = True, validators = [validate_password])

    class Meta:
        model = User
        fields = ["email", "password"]


class ProfileEditSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required =False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]
