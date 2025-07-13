\# Create Operation



>>> from bookshelf.models import Book

>>> book = Book.objects.create(title="1984", author="George Orwell", publication\_year=1949)

>>> book

\# <Book: 1984 by George Orwell (1949)>



\# Retrieve Operation



>>> book = Book.objects.first()

>>> book.title, book.author, book.publication\_year

\# ('1984', 'George Orwell', 1949)



\# Update Operation



>>> book = Book.objects.first()

>>> book.title = "Nineteen Eighty-Four"

>>> book.save()

>>> book

\# <Book: Nineteen Eighty-Four by George Orwell (1949)>



\# Delete Operation



>>> book = Book.objects.first()

>>> book.delete()

>>> Book.objects.all()

\# <QuerySet \[]>



