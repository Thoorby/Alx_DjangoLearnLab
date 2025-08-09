from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Book model.
    
    This serializer handles the serialization and deserialization of Book
    instances, including custom validation for the publication_year field
    to ensure it's not set to a future date.
    
    Custom Validation:
        - publication_year: Must not be in the future
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        This prevents logical errors where books are marked as
        published in years that haven't occurred yet.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            ValidationError: If publication year is in the future
        """
        current_year = datetime.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. "
                f"Current year is {current_year}."
            )
        
        # Optional: Add minimum year validation
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year seems too old. Please check the date."
            )
            
        return value
    
    def validate(self, data):
        """
        Object-level validation for the entire Book instance.
        
        This method can be used for validations that require
        access to multiple fields simultaneously.
        """
        # Example: Additional validation logic could go here
        return data


class AuthorSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Author model with nested Book serialization.
    
    This serializer demonstrates advanced DRF concepts by including
    a nested relationship. It serializes the Author model along with
    all associated Book instances using the BookSerializer.
    
    Nested Relationships:
        - books: Dynamically includes all books written by this author
        
    The relationship is handled through Django's related_name='books'
    defined in the Book model's ForeignKey field. This allows us to
    access an author's books via author.books.all().
    """
    
    # Nested serializer for related books
    # many=True indicates this is a one-to-many relationship
    # read_only=True means books are only serialized, not deserialized
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def validate_name(self, value):
        """
        Custom validation for the author's name.
        
        Ensures the name meets basic requirements.
        
        Args:
            value (str): The author's name to validate
            
        Returns:
            str: The validated name
            
        Raises:
            ValidationError: If name doesn't meet requirements
        """
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Author name must be at least 2 characters long."
            )
        
        return value.strip().title()  # Capitalize properly


class AuthorDetailSerializer(AuthorSerializer):
    """
    Extended Author serializer for detailed views.
    
    This serializer builds upon AuthorSerializer but includes
    additional computed fields and detailed book information.
    This demonstrates how to extend serializers for different
    use cases (list view vs detail view).
    """
    
    # Computed field: total number of books
    book_count = serializers.SerializerMethodField()
    
    # Include publication year range
    publication_year_range = serializers.SerializerMethodField()
    
    class Meta(AuthorSerializer.Meta):
        fields = AuthorSerializer.Meta.fields + [
            'book_count', 
            'publication_year_range'
        ]
    
    def get_book_count(self, obj):
        """
        Calculate the total number of books for this author.
        
        Args:
            obj (Author): The author instance
            
        Returns:
            int: Number of books written by this author
        """
        return obj.books.count()
    
    def get_publication_year_range(self, obj):
        """
        Calculate the range of publication years for this author.
        
        Args:
            obj (Author): The author instance
            
        Returns:
            dict: Contains 'earliest' and 'latest' publication years,
                  or None if author has no books
        """
        books = obj.books.all()
        if not books:
            return None
        
        years = [book.publication_year for book in books]
        return {
            'earliest': min(years),
            'latest': max(years)
        }


# Example of a write-enabled nested serializer
class AuthorWithBooksSerializer(serializers.ModelSerializer):
    """
    Serializer that allows creating/updating authors with books.
    
    This demonstrates how to handle nested writes, which is more
    complex than read-only nested serialization.
    """
    
    books = BookSerializer(many=True, required=False)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def create(self, validated_data):
        """
        Create author with associated books.
        
        This method handles the complexity of creating related
        objects in a single API call.
        """
        books_data = validated_data.pop('books', [])
        author = Author.objects.create(**validated_data)
        
        for book_data in books_data:
            Book.objects.create(author=author, **book_data)
        
        return author
    
    def update(self, instance, validated_data):
        """
        Update author and associated books.
        
        Note: This is a simplified implementation. In production,
        you might want more sophisticated handling of book updates.
        """
        books_data = validated_data.pop('books', [])
        
        # Update author fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Simple approach: clear existing books and recreate
        # In production, you might want to update existing books
        if books_data:
            instance.books.all().delete()
            for book_data in books_data:
                Book.objects.create(author=instance, **book_data)
        
        return instance