from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Product, ProductDetail, Category, Brand, ProductComment
from django.db.models import Min, Max
from .forms import CommentForm


class ProductListView( ListView ):
    model = Product
    template_name = 'product_module/product_list_page.html'
    paginate_by = 6

    def get_queryset(self, brand_name=None):
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'product list'
        context['brands'] = Brand.objects.all()
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


class ProductDetailView( DetailView ):
    model = Product
    template_name = 'product_module/product_detail_view_page.html'
    form_class = CommentForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'product detail'
        object = self.object
        details = ProductDetail.objects.filter( product=object ).all()
        # find min and max of prices
        min_max_price = details.aggregate( Min( 'price' ), Max( 'price' ) )
        context['price__min'], context['price__max'] = min_max_price.values()
        context['comments'] = ProductComment.objects.filter( product=object )
        context['comment_form'] = self.form_class( initial={'product': self.object} )
        related_products = [i for i in Product.objects.filter( brand=object.brand ) if i != object]
        context['related_products'] = related_products
        return context

    def post(self, *args, **kwargs):
        comment_form = self.form_class( self.request.POST )
        if comment_form.is_valid():
            comment_form.save()
        return HttpResponseRedirect( self.request.path_info )


def get_product_detail(request):
    # print( 'request', request.GET )
    product_id = request.GET.get( 'product_id' )
    detail_color = request.GET.get( 'color' )
    product = Product.objects.filter( id=product_id ).first()
    # product_detail = product.productdetail_set.filter( color=detail_color )
    product_detail = ProductDetail.objects.filter( product=product, color=detail_color ).first()
    context = {'price': product_detail.price}
    return JsonResponse( context )
