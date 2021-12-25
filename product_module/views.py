from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, ProductDetail, Category


class ProductListView( ListView ):
    model = Product
    template_name = 'product_module/product_list_page.html'


class ProductDetailView( DetailView ):
    model = Product
    template_name = 'product_module/product_detail_view_page.html'
