from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from products.models import Product, ProductCategory, Basket
from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator
from users.models import User
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView


# Create your views here.

class IndexView(TemplateView):
    template_name = 'products/index.html'
    title = 'StyleX'
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = 'StyleX'
        return context

# Ф-я index для отображения главной страницы
'''def index(request):
    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context=context)
'''

class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    
    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context =  super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'StyleX-Каталог'
        context['categories'] = ProductCategory.objects.all()
        context['cat_select'] = self.kwargs.get('category_id')
        return context

# Ф-я для отображения списка товаров по категориям, а такде для пагинации
'''def products(request, category_id=None, page=1):
    if category_id:
        products = ProductCategory.objects.get(pk=category_id).product_set.all()
    else:
        products = Product.objects.all()

    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page)    
    
    context = { 
            'title': 'Store-Каталог',
            'categories': ProductCategory.objects.all(), 
            'products': products_paginator
            }
    return render(request, 'products/products.html', context=context)'''


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(pk=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
   
 
@login_required   
def basket_remove(request, basket_id):
    basket = Basket.objects.get(pk=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
 