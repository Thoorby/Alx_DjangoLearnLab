from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions, filters as drf_filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Book, Author
from .serializers import BookSerializer, BookCreateUpdateSerializer, AuthorSerializer
from .permissions import IsOwnerOrReadOnly


class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Retrieve all books with filtering, searching, and ordering capabilities.
    """
    queryset = Book.objects.select_related('author', 'created_by').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_fields = {
        'title': ['exact', 'icontains'],
        'author': ['exact'],
        'genre': ['exact'],
        'publication_year': ['exact', 'gte', 'lte'],
        'is_available': ['exact'],
    }
    search_fields = ['title', 'description', 'author__name']
    ordering_fields = ['title', 'publication_date', 'price', 'created_at']
    ordering = ['-created_at']


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/{id}/
    Retrieve a single book by ID with full details.
    """
    queryset = Book.objects.select_related('author', 'created_by').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/
    Create a new book entry.
    """
    queryset = Book.objects.all()
    serializer_class = BookCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        book_serializer = BookSerializer(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Book created successfully', 'book': book_serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/{id}/
    Update an existing book.
    """
    queryset = Book.objects.all()
    serializer_class = BookCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        book_serializer = BookSerializer(serializer.instance)
        return Response({
            'message': 'Book updated successfully',
            'book': book_serializer.data
        })


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/{id}/
    Delete a book entry.
    """
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book_title = instance.title
        soft_delete = request.query_params.get('soft_delete', 'false').lower() == 'true'

        if soft_delete:
            instance.is_available = False
            instance.save()
            return Response({
                'message': f'Book "{book_title}" marked as unavailable',
                'soft_delete': True
            }, status=status.HTTP_200_OK)
        else:
            self.perform_destroy(instance)
            return Response({
                'message': f'Book "{book_title}" deleted successfully',
                'soft_delete': False
            }, status=status.HTTP_204_NO_CONTENT)


class MyBooksView(generics.ListAPIView):
    """GET /api/my-books/ - Books created by the current user"""
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user).select_related('author')


class BooksByGenreView(generics.ListAPIView):
    """GET /api/books/genre/{genre}/ - Books filtered by genre"""
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        genre = self.kwargs['genre']
        return Book.objects.filter(genre=genre).select_related('author', 'created_by')


class AuthorListView(generics.ListAPIView):
    """GET /api/authors/ - List all authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
    filter_backends = [drf_filters.SearchFilter, drf_filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):
    """GET /api/authors/{id}/ - Get author details"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
