from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import get_object_or_404
from .models import Book, Author
from .serializers import BookSerializer, BookCreateUpdateSerializer, AuthorSerializer
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly

class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Retrieve all books with filtering, searching, and ordering capabilities.
    
    Features:
    - Filtering by genre, author, is_available
    - Searching by title and description
    - Ordering by any field
    - Pagination support
    """
    queryset = Book.objects.select_related('author', 'created_by').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering options
    filterset_fields = ['genre', 'author', 'is_available']
    
    # Search functionality
    search_fields = ['title', 'description', 'author__name']
    
    # Ordering options
    ordering_fields = ['title', 'publication_date', 'price', 'created_at']
    ordering = ['-created_at']  # Default ordering

class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/{id}/
    Retrieve a single book by ID with full details.
    
    Features:
    - Public read access
    - Detailed book information including author details
    """
    queryset = Book.objects.select_related('author', 'created_by').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/
    Create a new book entry.
    
    Features:
    - Authentication required
    - Automatic assignment of created_by field
    - Comprehensive data validation
    """
    queryset = Book.objects.all()
    serializer_class = BookCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Override to automatically set the created_by field
        to the current authenticated user
        """
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Custom create method with enhanced response"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return full book details in response
        book_serializer = BookSerializer(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {
                'message': 'Book created successfully',
                'book': book_serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/{id}/
    Update an existing book.
    
    Features:
    - Authentication required
    - Owner-only access (user can only update books they created)
    - Supports both full (PUT) and partial (PATCH) updates
    """
    queryset = Book.objects.all()
    serializer_class = BookCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        """Custom update method with enhanced response"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return full book details in response
        book_serializer = BookSerializer(serializer.instance)
        
        return Response({
            'message': 'Book updated successfully',
            'book': book_serializer.data
        })

class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/{id}/
    Delete a book entry.
    
    Features:
    - Authentication required
    - Owner-only access (user can only delete books they created)
    - Soft delete option (marks as unavailable instead of actual deletion)
    """
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        """
        Custom delete method with confirmation response
        and optional soft delete
        """
        instance = self.get_object()
        book_title = instance.title
        
        # Check if soft delete is requested
        soft_delete = request.query_params.get('soft_delete', 'false').lower() == 'true'
        
        if soft_delete:
            # Soft delete: mark as unavailable
            instance.is_available = False
            instance.save()
            return Response({
                'message': f'Book "{book_title}" marked as unavailable',
                'soft_delete': True
            }, status=status.HTTP_200_OK)
        else:
            # Hard delete
            self.perform_destroy(instance)
            return Response({
                'message': f'Book "{book_title}" deleted successfully',
                'soft_delete': False
            }, status=status.HTTP_204_NO_CONTENT)

# Additional specialized views for advanced functionality

class MyBooksView(generics.ListAPIView):
    """
    GET /api/my-books/
    Retrieve books created by the authenticated user.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user).select_related('author')

class BooksByGenreView(generics.ListAPIView):
    """
    GET /api/books/genre/{genre}/
    Retrieve books filtered by a specific genre.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        genre = self.kwargs['genre']
        return Book.objects.filter(genre=genre).select_related('author', 'created_by')

# Author views for completeness
class AuthorListView(generics.ListAPIView):
    """GET /api/authors/ - List all authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class AuthorDetailView(generics.RetrieveAPIView):
    """GET /api/authors/{id}/ - Get author details"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]