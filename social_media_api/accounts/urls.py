from django.contrib.auth import login
from rest_framework import generics, permissions
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    # your implementation

class LoginView(generics.CreateAPIView):
    # your implementation

class ProfileView(generics.RetrieveAPIView):
    # your implementation