from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface for Author model.
    
    Provides a clean interface for managing authors and viewing
    their associated books.
    """
    list_display = ['name', 'book_count']
    search_fields = ['name']
    
    def book_count(self, obj):
        """Display number of books for each author."""
        return obj.books.count()
    book_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for Book model.
    
    Provides filtering and search capabilities for better
    book management.
    """
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_year', 'title']