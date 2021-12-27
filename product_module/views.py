from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, ProductDetail, Category, Brand


class ProductListView( ListView ):
    model = Product
    template_name = 'product_module/product_list_page.html'
    paginate_by = 6

    def get_queryset(self, brand_name=None):
        print( self.request, self.kwargs, brand_name, self.request.GET )
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'product list'
        context['brands'] = Brand.objects.all()
        return context


class ProductDetailView( DetailView ):
    model = Product
    template_name = 'product_module/product_detail_view_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'product detail'

        return context


# show products from newest to oldest
class NewProductListView( ListView ):
    model = Product
    template_name = 'product_module/product_list_page.html'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'new products'
        context['brands'] = Brand.objects.all()
        return context


class ProductByBrand( ListView ):
    model = Product
    template_name = 'product_module/product_list_page.html'
    paginate_by = 6
    ordering = ['id']

    def get_queryset(self, *, object_list=None, **kwargs):
        brand_name = self.kwargs.get( 'brand_name' )
        return Product.objects.filter( brand__title=brand_name ).order_by( '-added_date' )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'products by brand'
        context['brands'] = Brand.objects.all()
        return context
