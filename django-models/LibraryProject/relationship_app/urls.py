from django.urls import path
<<<<<<< HEAD
=======
from django.contrib.auth.views import LoginView, LogoutView
>>>>>>> 490bb1b1b4bc3491b1150b2a192077d7b3e3f17a
from . import views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
<<<<<<< HEAD
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
=======
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
>>>>>>> 490bb1b1b4bc3491b1150b2a192077d7b3e3f17a
]
