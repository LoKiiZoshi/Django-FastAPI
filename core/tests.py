from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Product, Order

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics',
            description='Electronic items'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(str(self.category), 'Electronics')

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product = Product.objects.create(
            name='Laptop',
            slug='laptop',
            description='Gaming laptop',
            category=self.category,
            price=999.99,
            stock=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Laptop')
        self.assertTrue(self.product.is_in_stock)

class APITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
