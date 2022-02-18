from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Product, ProductDetail, Category, Brand, ProductComment, Visited_Ip_product
from django.db.models import Min, Max, Q
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.list import MultipleObjectMixin


class ProductListView(ListView):
    model = Product
    template_name = 'product_module/product_list_page.html'
    paginate_by = 2

    def get_queryset(self):
        print(self.request.GET)
        print(self.kwargs)
        print(self.request)
        products = Product.objects.filter(is_active=True, is_delete=False)
        brand = self.request.GET.getlist('brand')
        category = self.request.GET.getlist('category')
        order = self.request.GET.getlist('order')
        if brand:
            products = products.filter(brand__title__in=brand)

        if category:
            products = products.filter(category__title__in=category)
        if order:
            if order == 'most-visit':
                products.order_by('visited_count')

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'product list'
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        return context


# show products from newest to oldest
class NewProductListView(ListView):
    model = Product
    template_name = 'product_module/product_list_page.html'
    paginate_by = 2

    def get_queryset(self):
        return Product.objects.all().order_by('-added_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'new products'
        context['brands'] = Brand.objects.all()
        return context


class ProductByBrand(ListView):
    model = Product
    template_name = 'product_module/product_list_page.html'
    paginate_by = 6
    ordering = ['id']

    def get_queryset(self, *, object_list=None, **kwargs):
        brand_name = self.kwargs.get('brand_name')
        return Product.objects.filter(brand__title=brand_name).order_by('-added_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'products by brand'
        context['brands'] = Brand.objects.all()
        return context


class ProductByCategory(ListView):
    model = Product
    template_name = 'product_module/product_list_page.html'
    paginate_by = 6
    ordering = ['id']

    def get_queryset(self, *, object_list=None, **kwargs):
        brand_name = self.kwargs.get('category_name')
        return Product.objects.filter(category__title=brand_name).order_by('-added_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'products by category'
        context['brands'] = Brand.objects.all()
        return context


# get user ip
def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ProductDetailView(DetailView, MultipleObjectMixin):
    model = Product
    template_name = 'product_module/product_detail_view_page.html'
    form_class = CommentForm
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        object = self.object
        comments = ProductComment.objects.filter(product=object)
        context = super().get_context_data(object_list=comments, **kwargs)
        context['title'] = 'product detail'
        details = ProductDetail.objects.filter(product=object).all()
        # find min and max of prices
        min_max_price = details.aggregate(Min('price'), Max('price'))
        context['price__min'], context['price__max'] = min_max_price.values()
        comments = ProductComment.objects.filter(product=object)
        context['comment_form'] = self.form_class(initial={'product': self.object})
        related_products = [i for i in Product.objects.filter(brand=object.brand).order_by('?') if i != object]
        context['related_products'] = related_products
        paginator = Paginator(comments, 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        ip = get_ip(self.request)
        visited_ip_product = Visited_Ip_product.objects.filter(product=self.object, user_ip=ip).all()
        if len(visited_ip_product) == 0:
            Visited_Ip_product.objects.create(product=self.object, user_ip=ip)
            self.object.visited_count += 1
            self.object.save()

        return context

    def post(self, *args, **kwargs):
        comment_form = self.form_class(self.request.POST)
        if comment_form.is_valid():
            comment_form.save()
        return HttpResponseRedirect(self.request.path_info)


def get_product_detail(request):
    # print( 'request', request.GET )
    product_id = request.GET.get('product_id')
    detail_color = request.GET.get('color')
    product = Product.objects.filter(id=product_id).first()
    # product_detail = product.productdetail_set.filter( color=detail_color )
    product_detail = ProductDetail.objects.filter(product=product, color=detail_color).first()
    context = {'price': product_detail.price, 'discount_price': product_detail.discount_price,
               'quantity': product_detail.quantity}
    return JsonResponse(context)


def product_list_by_search(request):
    query = request.GET['q']
    context = {
        'title': 'search products'
    }
    if query is not None:
        lookup = Q(title__icontains=query) | \
                 Q(brand__title__icontains=query) | \
                 Q(category__title__icontains=query)
        search_products = Product.objects.filter(lookup).distinct()
        context['page_obj'] = search_products
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        return render(request, 'product_module/product_list_page.html', context)
