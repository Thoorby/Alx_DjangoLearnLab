from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    # Book CRUD endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Additional book endpoints
    path('my-books/', views.MyBooksView.as_view(), name='my-books'),
    path('books/genre/<str:genre>/', views.BooksByGenreView.as_view(), name='books-by-genre'),
    
    # Author endpoints
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]
