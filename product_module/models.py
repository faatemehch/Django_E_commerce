from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q


class ProductManager(models.Manager):
    def get_product_by_filter(self, category_name=None, brand_name=None):
        lookup = Q(category__title=category_name) | Q(brand__title=brand_name)
        return self.get_queryset().filter(lookup).distinct()


class Brand(models.Model):
    title = models.CharField(max_length=200)
    logo_brand = models.ImageField(null=True, blank=True, upload_to='brand_logo/')

    class Meta:
        verbose_name = 'Product Brand'
        verbose_name_plural = 'Product Brands List'

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.title


class ProductDetail(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                help_text='product that related to the current detail')
    price = models.FloatField(default=0, verbose_name='product price')
    discount_price = models.FloatField(verbose_name='product discount price',
                                       help_text='discount price for a product', null=True, blank=True)
    image = models.ImageField(verbose_name='product image', upload_to='products_image/', null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='product activation')
    quantity = models.IntegerField(verbose_name='product quantity', help_text='number of current product')
    color = models.CharField(max_length=100, verbose_name='product color')
    size = models.CharField(max_length=100, verbose_name='product size')

    class Meta:
        verbose_name = 'Product Details'
        verbose_name_plural = 'Product Details List'

    def __str__(self):
        return f'{self.price}'


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='product title', db_index=True)
    main_image = models.ImageField(verbose_name='main image', help_text='main image of the current product', null=True,
                                   blank=True, upload_to='product_images_main/')
    short_description = models.CharField(max_length=500, verbose_name='product short description')
    description = models.TextField(verbose_name='product description')
    added_date = models.DateTimeField(auto_now_add=True, verbose_name='product added date')
    slug = models.SlugField(unique=True, db_index=True, null=False, default='', blank=True)
    category = models.ForeignKey(Category, verbose_name='product category',
                                 db_index=True, on_delete=models.CASCADE, null=True, blank=True)
    sell_count = models.IntegerField(default=0, null=True, blank=True, help_text='Number of product sales')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_index=True, null=True)
    visited_count = models.IntegerField(help_text='number of visited this product', default=0)
    is_delete = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=True, null=True)
    # objects = ProductManager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product List'

    def get_absolute_url(self):
        return reverse('product_module:product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=300)
    email = models.EmailField()
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product comment'
        verbose_name_plural = 'product comment list'
        ordering = ['created_date']

    def __str__(self):
        return self.fullname


# save visited ip addresses
class Visited_Ip_product(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    user_ip = models.TextField(verbose_name='ip address', help_text='user ip address')

    def __str__(self):
        return self.user_ip

    class Meta:
        verbose_name = 'ip address'
        verbose_name_plural = 'users ip address'
