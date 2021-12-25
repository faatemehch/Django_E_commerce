from django.db import models
from django.utils.text import slugify


class Category( models.Model ):
    title = models.CharField( max_length=200 )

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.title


class ProductDetail( models.Model ):
    product = models.ForeignKey( 'Product', on_delete=models.CASCADE,
                                 help_text='product that related to the current detail' )
    price = models.FloatField( default=0, verbose_name='product price' )
    discount_price = models.FloatField( verbose_name='product discount price',
                                        help_text='discount price for a product', null=True, blank=True )
    image = models.ImageField( verbose_name='product image', upload_to='products_image/', null=True, blank=True )
    is_active = models.BooleanField( default=False, verbose_name='product activation' )
    quantity = models.IntegerField( verbose_name='product quantity', help_text='number of current product' )
    color = models.CharField( max_length=100, verbose_name='product color' )
    size = models.CharField( max_length=100, verbose_name='product size' )

    class Meta:
        verbose_name = 'Product Details'
        verbose_name_plural = 'Product Details List'

    def __str__(self):
        return f'{self.product}'


class Product( models.Model ):
    title = models.CharField( max_length=300, verbose_name='product title', db_index=True )
    short_description = models.CharField( max_length=500, verbose_name='product short description' )
    description = models.TextField( verbose_name='product description' )
    added_date = models.DateTimeField( auto_now_add=True, verbose_name='product added date' )
    slug = models.SlugField( unique=True, db_index=True, null=False, default='', blank=True )
    categories = models.ManyToManyField( Category, verbose_name='product category',
                                         db_index=True,
                                         null=True, blank=True )
    sell_count = models.IntegerField( default=0, null=True, blank=True, help_text='Number of product sales' )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product List'

    def save(self, *args, **kwargs):
        self.slug = slugify( self.title )
        super( Product, self ).save( *args, **kwargs )

    def __str__(self):
        return f'{self.title}'
