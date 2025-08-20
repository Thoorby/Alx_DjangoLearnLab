from django.contrib.auth import get_user_model
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer

User = get_user_model()


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        return Response({"message": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        if user_to_unfollow == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user_to_unfollow)
        return Response({"message": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)


class MyFollowingListView(generics.ListAPIView):
    """
    Convenience endpoint to see who I'm following.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer  # you can use a slim serializer if you have one

    def get_queryset(self):
        return self.request.user.following.all()

