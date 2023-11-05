from django.urls import path
from .views import RegistrationView, LoginView, ProfileView, ProfileEditView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/view/', ProfileView.as_view(), name='profile-view'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile-edit-view'),
]
