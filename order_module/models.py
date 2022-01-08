from django.contrib.auth.models import User
from django.db import models
from product_module.models import Product, ProductDetail


class Order( models.Model ):
    owner = models.ForeignKey( User, on_delete=models.CASCADE )
    is_paid = models.BooleanField( default=False, help_text='order paid or not' )
    is_send = models.BooleanField( default=False, help_text='order sent or not' )
    created_date = models.DateTimeField( help_text='created current user order', auto_now_add=True )
    payment_date = models.DateTimeField( null=True, blank=True, help_text='order payment date' )
    tracking_code = models.CharField( null=True, max_length=50 )
    coupon_code = models.ForeignKey( 'Coupon', null=True, on_delete=models.DO_NOTHING, blank=True )

    # complete order
    name = models.CharField( max_length=50, null=True, blank=True )
    family = models.CharField( max_length=50, null=True, blank=True )
    post_code = models.IntegerField( null=True, blank=True )
    phone_number = models.IntegerField( null=True, blank=True )
    province = models.ForeignKey( 'Province', on_delete=models.CASCADE, null=True, blank=True )
    city = models.ForeignKey( 'City', on_delete=models.CASCADE, null=True, blank=True )
    address = models.TextField( null=True, blank=True )
    description = models.TextField( null=True, blank=True )

    def get_total_price(self):
        amount = 0
        for detail in self.orderdetail_set.all():
            amount += detail.price * detail.count
        if self.coupon_code is not None:
            amount -= (amount * self.coupon_code.amount) / 100
        return amount

    class Meta:
        verbose_name = 'user order'
        verbose_name_plural = 'orders list'

    def __str__(self):
        return self.owner.username


class OrderDetail( models.Model ):
    order = models.ForeignKey( Order, on_delete=models.CASCADE )
    product = models.ForeignKey( Product, on_delete=models.CASCADE )
    product_detail = models.ForeignKey( ProductDetail, on_delete=models.CASCADE )
    price = models.IntegerField( null=True )
    count = models.IntegerField( null=True )

    class Meta:
        verbose_name = 'order detail'
        verbose_name_plural = 'order detail lists'

    def __str__(self):
        return f'{self.product}'


class Province( models.Model ):
    province_name = models.CharField( max_length=30 )

    def __str__(self):
        return self.province_name

    class Meta:
        verbose_name = 'province'
        verbose_name_plural = 'provinces'


class City( models.Model ):
    province = models.ForeignKey( Province, on_delete=models.CASCADE )
    city_name = models.CharField( max_length=30 )

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'


class Coupon( models.Model ):
    code = models.CharField( max_length=10 )
    amount = models.IntegerField()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'discount code'
        verbose_name_plural = 'coupon codes'
