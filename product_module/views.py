from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, ProductDetail, Category


class ProductListView( ListView ):
    model = Product
    template_name = 'product_module/product_list_page.html'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'product list'
        return context


class ProductDetailView( DetailView ):
    model = Product
    template_name = 'product_module/product_detail_view_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'product detail'
        return context
