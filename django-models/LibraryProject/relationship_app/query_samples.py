import os
import django

# Set the correct settings module (case sensitive!)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# ... (author query here)

library_name = "Central City Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()

print(f"\nBooks in {library_name}:")
for book in books_in_library:
    print(f"- {book.title}")