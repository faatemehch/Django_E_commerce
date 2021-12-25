from django.contrib import admin
from . import models


class ProductTabular( admin.TabularInline ):
    model = models.ProductDetail


class ProductAdmin( admin.ModelAdmin ):
    inlines = [ProductTabular]
    list_display = ('__str__', 'added_date', 'slug')


class ProductDetailAdmin( admin.ModelAdmin ):
    list_display = ('__str__', 'price', 'discount_price', 'is_active')


admin.site.register( models.Product, ProductAdmin )
admin.site.register( models.ProductDetail, ProductDetailAdmin )
admin.site.register( models.Category )
