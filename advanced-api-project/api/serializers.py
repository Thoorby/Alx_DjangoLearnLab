from rest_framework import serializers
from .models import Book, Author
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model with nested book count"""
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'birth_date', 'email', 'books_count', 'created_at']
        read_only_fields = ['created_at']
    
    def get_books_count(self, obj):
        return obj.books.count()

class BookSerializer(serializers.ModelSerializer):
    """
    Comprehensive Book serializer with nested author information
    and custom validation
    """
    author_name = serializers.CharField(source='author.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_name', 'isbn', 
            'publication_date', 'genre', 'price', 'description', 
            'pages', 'is_available', 'created_by', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def validate_isbn(self, value):
        """Custom validation for ISBN format"""
        if not value.isdigit() or len(value) not in [10, 13]:
            raise serializers.ValidationError(
                "ISBN must be 10 or 13 digits long."
            )
        return value
    
    def validate_price(self, value):
        """Ensure price is positive"""
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )
        return value
    
    def validate_pages(self, value):
        """Ensure pages count is reasonable"""
        if value <= 0 or value > 10000:
            raise serializers.ValidationError(
                "Pages must be between 1 and 10,000."
            )
        return value

class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Specialized serializer for create/update operations"""
    
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'publication_date', 
            'genre', 'price', 'description', 'pages', 'is_available'
        ]
    
    def validate(self, data):
        """Cross-field validation"""
        from datetime import date
        
        if data.get('publication_date') and data['publication_date'] > date.today():
            raise serializers.ValidationError(
                "Publication date cannot be in the future."
            )
        return data