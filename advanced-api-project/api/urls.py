from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    # List all books
    path('books/', BookListView.as_view(), name='book-list'),

    # Retrieve a single book by ID (GET)
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # Create a new book (POST)
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # Update a book (PUT/PATCH - expects ID in request body)
    path('books/update/', BookUpdateView.as_view(), name='book-update'),

    # Delete a book (DELETE - expects ID in request body)
    path('books/delete/', BookDeleteView.as_view(), name='book-delete'),
]