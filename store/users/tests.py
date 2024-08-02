from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from users.models import User


class UserRegisterViewTestCase(TestCase):
    
    def setUp(self) -> None:
        self.path = reverse('users:registr')
        
    def test_user_register_get(self):
        responce = self.client.get(self.path)
        
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(responce, 'users/register.html')
        
    def test_user_register_post_success(self):
        
        data = {
            'first_name': 'Azamat', 'last_name': 'Azamatov',
            'username': 'povelas', 'email': 'as@gmail.com',
            'password1': '1256pP!', 'password2': '1256pP!',
        }
        
        username = data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        responce = self.client.post(self.path, data)
        
        self.assertEqual(responce.status_code, HTTPStatus.FOUND)
        self.assertRedirects(responce, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())