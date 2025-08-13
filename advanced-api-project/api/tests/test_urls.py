from django.urls import reverse, resolve
from django.test import SimpleTestCase
from api import views

class TestBookURLs(SimpleTestCase):

    def test_book_list_url(self):
        url = reverse('book-list')
        self.assertEqual(resolve(url).func.view_class, views.BookListView)

    def test_book_detail_url(self):
        url = reverse('book-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, views.BookDetailView)

    def test_book_create_url(self):
        url = reverse('book-create')
        self.assertEqual(resolve(url).func.view_class, views.BookCreateView)

    def test_book_update_url(self):
        url = reverse('book-update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, views.BookUpdateView)

    def test_book_delete_url(self):
        url = reverse('book-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, views.BookDeleteView)
