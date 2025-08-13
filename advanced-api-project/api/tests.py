from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book
import json
from datetime import date

class BookAPITestCase(APITestCase):
    """Comprehensive test suite for Book API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123',
            email='user1@test.com'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123',
            email='user2@test.com'
        )
        
        # Create test author
        self.author = Author.objects.create(
            name='Test Author',
            email='author@test.com',
            birth_date=date(1970, 1, 1)
        )
        
        # Create test book
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            isbn='1234567890123',
            publication_date=date(2023, 1, 1),
            genre='fiction',
            price=19.99,
            description='A test book',
            pages=200,
            created_by=self.user1
        )
    
    def test_book_list_view(self):
        """Test GET /api/books/"""
        url = reverse('api:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_book_detail_view(self):
        """Test GET /api/books/{id}/"""
        url = reverse('api:book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_book_create_authenticated(self):
        """Test POST /api/books/ with authentication"""
        self.client.force_authenticate(user=self.user1)
        
        data = {
            'title': 'New Book',
            'author': self.author.pk,
            'isbn': '9876543210987',
            'publication_date': '2024-01-01',
            'genre': 'mystery',
            'price': 24.99,
            'description': 'A new test book',
            'pages': 300,
            'is_available': True
        }
        
        url = reverse('api:book-create')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_book_create_unauthenticated(self):
        """Test POST /api/books/ without authentication"""
        data = {
            'title': 'New Book',
            'author': self.author.pk,
            'isbn': '9876543210987',
            'publication_date': '2024-01-01',
            'genre': 'mystery',
            'price': 24.99,
            'pages': 300
        }
        
        url = reverse('api:book-create')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_book_update_owner(self):
        """Test PUT/PATCH /api/books/{id}/ by owner"""
        self.client.force_authenticate(user=self.user1)
        
        data = {
            'title': 'Updated Book Title',
            'price': 29.99
        }
        
        url = reverse('api:book-update', kwargs={'pk': self.book.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book Title')
        self.assertEqual(float(self.book.price), 29.99)
    
    def test_book_update_non_owner(self):
        """Test PUT/PATCH /api/books/{id}/ by non-owner"""
        self.client.force_authenticate(user=self.user2)
        
        data = {'title': 'Unauthorized Update'}
        
        url = reverse('api:book-update', kwargs={'pk': self.book.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_delete_owner(self):
        """Test DELETE /api/books/{id}/ by owner"""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('api:book-delete', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
    
    def test_book_soft_delete(self):
        """Test soft delete functionality"""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('api:book-delete', kwargs={'pk': self.book.pk})
        response = self.client.delete(url + '?soft_delete=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.book.refresh_from_db()
        self.assertFalse(self.book.is_available)
    
    def test_book_filtering(self):
        """Test book filtering functionality"""
        url = reverse('api:book-list')
        
        # Test genre filtering
        response = self.client.get(url + '?genre=fiction')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Test author filtering
        response = self.client.get(url + f'?author={self.author.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_book_searching(self):
        """Test book search functionality"""
        url = reverse('api:book-list')
        
        # Test title search
        response = self.client.get(url + '?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_my_books_view(self):
        """Test GET /api/my-books/"""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('api:my-books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)