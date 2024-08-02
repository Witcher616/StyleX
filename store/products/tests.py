from django.test import TestCase
from django.urls import reverse
from products.models import Product, ProductCategory

class IndexViewTestCase(TestCase):
    
    def test_view(self):
        path = reverse('index')
        responce = self.client.get(path)
        
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.context_data['title'], 'Store')
        self.assertTemplateUsed(responce, 'products/index.html')
        
class ProductsListTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']
    
    def setUp(self) -> None:
       self.products = Product.objects.all()
    
    def test_list(self):
        path = reverse('products:index')
        responce = self.client.get(path)
        
        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, 'products/products.html')
        self.assertEqual(responce.context_data['title'], 'Store-Каталог')
        self.assertEqual(list(responce.context_data['object_list']), list(self.products[:3]))
        
    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        responce = self.client.get(path)
        
        
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.context_data['title'], 'Store-Каталог')
        self.assertTemplateUsed(responce, 'products/products.html')
        self.assertEqual(
            list(responce.context_data['object_list']),
            list(self.products.filter(category_id=category.id)[:3])
        )
        
        