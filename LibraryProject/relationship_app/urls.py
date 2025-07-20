from django.urls import path
from . import views

urlpatterns = [
    # Book listing
    path('books/', views.list_books, name='list_books'),

    # Library details (using DetailView)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # User authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
