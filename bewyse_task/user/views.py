from decouple import config
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer, ProfileEditSerializer
import firebase_admin
from django.contrib.auth.models import User
from firebase_admin import credentials
from .utils import isUnique
import requests
import json
from django.shortcuts import redirect


FIREBASE_API_KEY = config('FIREBASE_API_KEY')
PATH_TO_CERT = config('PATH_TO_CERT')

cred = credentials.Certificate(PATH_TO_CERT)
firebase_admin.initialize_app(cred)

class RegistrationView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get("email")
            password = request.data.get("password")
            username = request.data.get("username")
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            try:
                user = isUnique(username)
                if user:
                    return Response({"error":"A user with that username already exists."})
            except:
                pass
            if first_name is None:
                first_name = ""
            if last_name is None:
                last_name = ""
            if len(password) < 8:
                return Response({"error": "This password is too short. It must contain at least 8 characters."})       
            
            data = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, data=json.dumps(data))
            if response.status_code == 200:
                user_data = response.json()
                user_obj = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                )
                user_obj.save()              
                response_data = {
                    "username": username,
                    "email" : email,
                    }
                
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"There was an error creating the user"}, status=status.HTTP_404_NOT_FOUND)
        if "email" in serializer.errors:
            error = serializer.errors.get('email', [''])[0]
            return Response({"error":f"Email:{error}"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if "password" in serializer.errors:
            error = serializer.errors.get('password', [''])[0]
            return Response({"error":f"Password:{error}"}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        if serializer.is_valid():
            email = request.data["email"]
            password = request.data["password"]

            data = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, data=json.dumps(data))
            if response.status_code == 200:
                user_data = response.json()
                id_token = user_data.get("idToken")
                email = user_data.get("email")
                user = User.objects.get(email=email)
                serializer = UserProfileSerializer(user)
                data = serializer.data
                if user.username is None:
                    data['username'] = ""
                if user.first_name is None or user.last_name is None:
                    data['full_name'] = ""
                data['custom_token'] = id_token
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Email or password is invalid.'},status=status.HTTP_401_UNAUTHORIZED)
            

class ProfileView(APIView):
    def get(self, request):
        try:
            user = request.authenticated_user
            username = request.GET.get('username')  #Passing username as parameter eg. http://127.0.0.1:8000/accounts/profile/view/?username=<admin>
            user = User.objects.get(username=username)
            serializer = UserProfileSerializer(user)
            data = serializer.data
            if user.first_name is None and user.last_name is None:
                data['full_name'] = ""
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Unauthorized request.'},status=status.HTTP_401_UNAUTHORIZED)


class ProfileEditView(APIView):
    serializer_class = ProfileEditSerializer
    def post(self,request):
        user = request.authenticated_user
        serializer = ProfileEditSerializer(data=request.data)
        if serializer.is_valid():
            email = user.email
            user = User.objects.get(email=email)
            response = {}
            
            try:
                first_name = request.data.get("first_name")
                if first_name:
                    user.first_name = first_name
                    # response["first_name"] = first_name
            except:
                pass
            try:
                last_name = request.data.get("last_name")
                if last_name:
                    user.last_name = last_name
                    # response["last_name"] = last_name
            except:
                pass
            try:
                username = request.data.get("username")
                if username:
                    if isUnique(username) is not None:
                        return Response({"error":"A user with that username already exists."})
                    else:
                        user.username = username
            except:
                pass
            user.save()
            response["email"] = email
            if user.username is None:
                response["username"] = ""
            else:
                response["username"] = user.username
            if user.first_name is None and user.last_name is None:
                response["full_name"] = ""
            else:
                serializer = UserProfileSerializer(user)
                data = serializer.data
                response["full_name"] = data["full_name"]
            return Response(response, status=status.HTTP_200_OK)
        return JsonResponse({"error":"There was error saving the details"}, status=status.HTTP_401_UNAUTHORIZED)

