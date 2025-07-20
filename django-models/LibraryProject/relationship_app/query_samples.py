import os
import django

# Set the correct settings module (case sensitive!)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Now you can query like this:
author_name = "Chinua Achebe"
author = Author.objects.get(name=author_name)
books_by_author = author.books.all()

print(f"Books by {author_name}:")
for book in books_by_author:
    print(f"- {book.title}")

# ... add other queries
