from django.http import JsonResponse
from firebase_admin import auth


class FirebaseAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            authenticated_user = self.authenticate(token)
            if authenticated_user:
                request.authenticated_user = authenticated_user
            else:
                return JsonResponse({"error": "Unauthorized"}, status=401)
        response = self.get_response(request)
        return response

    def authenticate(self, token):
        try:
            token = token.split(" ").pop()
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
            user = auth.get_user(uid=uid)
            return user   
        except Exception:
            return None
