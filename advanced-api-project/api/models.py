from django.db import models
from datetime import datetime

class Author(models.Model):
    """
    Author model representing book authors.
    
    This model stores basic author information and serves as the parent
    in a one-to-many relationship with the Book model. Each author can
    have multiple books associated with them.
    
    Fields:
        name (str): The full name of the author
    """
    name = models.CharField(
        max_length=100,
        help_text="Full name of the author"
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing individual books.
    
    This model stores book information and establishes a many-to-one
    relationship with the Author model. Each book belongs to exactly
    one author, but an author can have multiple books.
    
    Fields:
        title (str): The title of the book
        publication_year (int): Year the book was published
        author (ForeignKey): Reference to the Author who wrote this book
    """
    title = models.CharField(
        max_length=200,
        help_text="Title of the book"
    )
    publication_year = models.IntegerField(
        help_text="Year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',  # This allows reverse lookup: author.books.all()
        help_text="Author who wrote this book"
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-publication_year', 'title']
        # Ensure no duplicate books for the same author
        unique_together = ['title', 'author']