from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from django.contrib.auth.models import User

def isAuthenticated(request, custom_token):
    if not custom_token:
        return Response("Token does not exist",  status=status.HTTP_401_UNAUTHORIZED)
    token = custom_token.split(" ").pop()
    decoded_token=None
    try:
        decoded_token = auth.verify_id_token(token)
    except Exception:
        return Response("Invalid Token", status=status.HTTP_401_UNAUTHORIZED)
    if not custom_token or not decoded_token:
        return None
    try:
        uid = decoded_token.get('uid')
        user = auth.get_user(uid=uid)
        return user
    except Exception:
        return Response("Uid not available", status=status.HTTP_401_UNAUTHORIZED)
    

def isUnique(username):
    try:
        user = User.objects.get(username=username)
        if user:
            return user
    except User.DoesNotExist:
        return None

