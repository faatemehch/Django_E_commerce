from django.contrib import admin
from . import models


class ProductTabularDetail( admin.TabularInline ):
    model = models.ProductDetail


class ProductAdmin( admin.ModelAdmin ):
    inlines = [ProductTabularDetail]
    list_display = ('__str__', 'added_date', 'brand')


class ProductDetailAdmin( admin.ModelAdmin ):
    list_display = ('__str__', 'price', 'discount_price', 'is_active')


admin.site.register( models.Product, ProductAdmin )
admin.site.register( models.ProductDetail, ProductDetailAdmin )
admin.site.register( models.Category )
admin.site.register( models.Brand )
