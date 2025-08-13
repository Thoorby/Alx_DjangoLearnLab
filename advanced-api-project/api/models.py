from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    """Author model for the Book API"""
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Book(models.Model):
    """Book model with comprehensive fields for API operations"""
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
        ('sci_fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('biography', 'Biography'),
        ('history', 'History'),
    ]
    
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    pages = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    class Meta:
        ordering = ['-created_at', 'title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['genre']),
        ]