from django.urls import path
from . import views

urlpatterns = [
    # Book list function-based view
    path('books/', views.list_books, name='list_books'),
    
    # Library detail class-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication routes using your function-based views
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
