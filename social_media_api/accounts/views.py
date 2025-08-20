from django.contrib.auth import get_user_model
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSlimSerializer

User = get_user_model()


class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int):
        target = generics.get_object_or_404(User, pk=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.follow(target)
        return Response({"detail": f"Followed {target.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int):
        target = generics.get_object_or_404(User, pk=user_id)
        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.unfollow(target)
        return Response({"detail": f"Unfollowed {target.username}."}, status=status.HTTP_200_OK)


class MyFollowingListView(generics.ListAPIView):
    """
    Optional convenience endpoint to see who I'm following.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSlimSerializer

    def get_queryset(self):
        return self.request.user.following.all()
