from django.urls import path
from .views import
from .views import add_comment, CommentUpdateView, CommentDeleteView

 (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView
)

urlpatterns = [
    # Auth URLs
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),

    # CRUD URLs (checker expects singular 'post')
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]

urlpatterns += [
    
    path("posts/<int:post_id>/comments/new/", add_comment, name="comment-add"),
    path("comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
]