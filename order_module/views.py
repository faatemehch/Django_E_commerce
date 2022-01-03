from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from product_module.models import Product, ProductDetail
from .models import Order, OrderDetail
import random
import string


def create_tracking_code():
    # create tracking code
    return ''.join( random.choices( string.ascii_lowercase + string.digits, k=20 ) )


@login_required
def add_user_order(request):
    order_form_data = request.POST  # get form info (POST request)
    # get product order details
    product: Product = Product.objects.filter( id=order_form_data['product'] ).first()
    product_detail = product.productdetail_set.filter( color=order_form_data['product-color'] ).first()
    # find or create an open order
    order: Order = Order.objects.filter( owner=request.user, is_paid=False ).first()
    if order is None:
        order: Order = Order.objects.create( owner=request.user,
                                             tracking_code=f'{create_tracking_code}+{request.user.id}' )
    order_detail: OrderDetail = order.orderdetail_set.filter( product=product, product_detail=product_detail ).first()
    if order_detail is None:
        order_detail = order.orderdetail_set.create( product=product, product_detail=product_detail,
                                                     count=order_form_data['quantity'] )
    else:
        order_detail.count += int( order_form_data['quantity'] )
        if product_detail.discount_price:
            order_detail.price = product_detail.discount_price
        else:
            order_detail.price = product_detail.price
        order_detail.save()
    return redirect( 'home_module:home-view' )
