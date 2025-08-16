from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create an author
        self.author = Author.objects.create(name='Test Author', email='author@test.com')
        
        # Create a book
        self.book = Book.objects.create(
            title='Test Book',
            description='A book for testing',
            genre='fiction',
            publication_date='2023-01-01',
            price=10.0,
            is_available=True,
            author=self.author,
            created_by=self.user,
            pages=100
        )
        
        self.create_url = reverse('book-create')
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})
        self.update_url = reverse('book-update', kwargs={'pk': self.book.pk})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book.pk})

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'New Book',
            'description': 'Another test book',
            'genre': 'non-fiction',
            'published_date': '2023-06-01', 
            'price': 15.0,
            'is_available': True,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['book']['title'], 'New Book')

    def test_update_book(self):
        self.client.login(username='testuser', password='testpass')
        data = {'title': 'Updated Book'}
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['book']['title'], 'Updated Book')

    def test_delete_book(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    def test_permissions_required(self):
        # Logout to test unauthenticated access
        self.client.logout()
        response = self.client.post(self.create_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_books(self):
        response = self.client.get(f'{self.list_url}?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_ordering_books(self):
        response = self.client.get(f'{self.list_url}?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_books_by_genre(self):
        response = self.client.get(reverse('books-by-genre', kwargs={'genre': 'fiction'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
