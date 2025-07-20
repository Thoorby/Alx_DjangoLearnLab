import sys
import os
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

# Set the correct Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

# Setup Django
django.setup()

# Your model queries here
from relationship_app.models import Author, Book, Library, Librarian

# Example queries (keep yours here)
print("Setup successful.")

def run_queries():
    # 1. Query all books by a specific author
    author_name = "Chinua Achebe"
    try:
        author = Author.objects.get(name=author_name)
        books_by_author = author.books.all()
        print(f"Books by {author_name}:")
        for book in books_by_author:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with name {author_name}")

    # 2. List all books in a library
    library_name = "Central City Library"
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"\nBooks in {library_name}:")
        for book in books_in_library:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"No library found with name {library_name}")

    # 3. Retrieve the librarian for a library
    try:
        librarian = library.librarian
        print(f"\nLibrarian of {library_name}: {librarian.name}")
    except Library.librarian.RelatedObjectDoesNotExist:
        print(f"No librarian assigned to {library_name}")

if __name__ == "__main__":
    run_queries()
