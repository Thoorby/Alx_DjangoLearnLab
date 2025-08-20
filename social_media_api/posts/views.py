from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions, generics

# Custom permission to allow only owners to edit/delete
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS → allow anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Otherwise, only the owner/author can modify
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

User = get_user_model()

class FeedView(generics.ListAPIView):
    """
    Returns a feed of posts created by users the current user follows.
    Ordered newest-first. Paginated via DRF settings.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        u = self.request.user
        following_ids = u.following.values_list('id', flat=True)

        # Followed users only:
        qs = Post.objects.filter(author_id__in=following_ids)

        # If you also want to include the user's own posts in the feed, uncomment:
        # qs = Post.objects.filter(author_id__in=list(following_ids) + [u.id])

        return qs.select_related('author').order_by('-created_at')

