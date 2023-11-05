
from django.contrib import admin
from django.urls import path, include
from user import urls as user_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("accounts/", include(user_urls)),
]
