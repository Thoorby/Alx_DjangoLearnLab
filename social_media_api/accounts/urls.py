from django.urls import path
from django.contrib.auth import login
from .views import FollowUserView, UnfollowUserView, MyFollowingListView
from rest_framework import generics, permissions
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    # your implementation

class LoginView(generics.CreateAPIView):
    # your implementation

class ProfileView(generics.RetrieveAPIView):
    # your implementation

urlpatterns = [
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('following/', MyFollowingListView.as_view(), name='my_following'),
]
