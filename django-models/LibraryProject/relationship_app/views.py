from django.shortcuts import render, get_object_or_404
from .models import Book, Library  # Assuming you have a Library model too
from django.views.generic import DetailView

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_book.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

