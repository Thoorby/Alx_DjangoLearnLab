<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404
from .models import Book, Library  # Assuming you have a Library model too
from django.views.generic import DetailView

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

=======
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Registration view renamed to 'register'
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after register
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
>>>>>>> 490bb1b1b4bc3491b1150b2a192077d7b3e3f17a
