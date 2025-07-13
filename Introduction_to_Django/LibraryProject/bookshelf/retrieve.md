\# Retrieve Operation



>>> from bookshelf.models import Book

>>> book = Book.objects.first()

>>> book.title, book.author, book.publication\_year

\# ('1984', 'George Orwell', 1949)



