from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'birth_date', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email']
    ordering = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'price', 'is_available', 'created_at']
    list_filter = ['genre', 'is_available', 'publication_date', 'created_at']
    search_fields = ['title', 'author__name', 'isbn']
    list_editable = ['is_available', 'price']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn', 'publication_date')
        }),
        ('Content Details', {
            'fields': ('genre', 'description', 'pages')
        }),
        ('Publishing Information', {
            'fields': ('price', 'is_available')
        }),
        ('System Information', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )
