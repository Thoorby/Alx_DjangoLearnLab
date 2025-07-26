# relationship_app/urls.py
from django.urls import path
from . import views  # ✅ this allows access to views.book_list
from .views import LibraryDetailView

urlpatterns = [
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('books/', views.book_list, name='book-list'),  # ✅ Function-Based View
]

