from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from product_module.models import Product, ProductDetail
from .models import Order, OrderDetail, Coupon, Province, City
import random
import string
from .forms import CompleteForm


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

    product_detail.quantity -= int( order_form_data['quantity'] )
    product_detail.save()
    order_detail.save()
    return redirect( 'home_module:home-view' )


@login_required
def user_open_order(request):
    # if user doesn't pay the order is open
    context = {
        'title': f'{request.user.username} open order'
    }
    open_order = Order.objects.filter( owner=request.user, is_paid=False ).first()
    if open_order is None:
        return redirect( 'home_module:home-view' )
    context['open_order'] = open_order
    return render( request, 'order_module/user_open_order_list.html', context )


@login_required
def delete_order_item(request, order_detail_id):
    order_detail: OrderDetail = OrderDetail.objects.filter( id=order_detail_id ).first()
    if order_detail is not None and not order_detail.order.is_paid:
        order_detail.product_detail.quantity += order_detail.count
        order_detail.product_detail.save()
        order_detail.delete()
    return redirect( 'order_module:user-open-order' )


@login_required
def decrease_item_counter(request, order_detail_id):
    '''
        decrease counter of an order detail
    '''
    order_detail: OrderDetail = OrderDetail.objects.filter( id=order_detail_id ).first()
    if order_detail is not None and not order_detail.order.is_paid:
        order_detail.product_detail.quantity += 1
        order_detail.product_detail.save()
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    return redirect( 'order_module:user-open-order' )


@login_required
def increase_item_counter(request, order_detail_id):
    '''
        decrease counter of an order detail
    '''
    order_detail: OrderDetail = OrderDetail.objects.filter( id=order_detail_id ).first()
    if order_detail is not None and not order_detail.order.is_paid:
        if order_detail.product_detail.quantity == 0:
            return redirect( 'order_module:user-open-order' )
        order_detail.product_detail.quantity -= 1
        order_detail.product_detail.save()
        order_detail.count += 1
        order_detail.save()
    return redirect( 'order_module:user-open-order' )


@login_required
def add_coupon_code(request):
    open_order: Order = Order.objects.filter( owner=request.user, is_paid=False ).first()
    if open_order is not None:
        if open_order.coupon_code is None:
            coupon_form = request.POST['coupon']
            coupon = Coupon.objects.filter( code=coupon_form ).first()
            if coupon is not None:
                open_order.coupon_code = coupon
                open_order.save()
                context = {'message': 'coupon code added successfully!', 'total': open_order.get_total_price()}
            else:
                context = {'message': 'coupon code not found!'}
        else:
            context = {'message': 'you used coupon code before!'}
    else:
        context = {'message': 'something went wrong!'}
    return JsonResponse( context )


def get_cities(request, ):
    cities = City.objects.filter( province_id=request.GET.get( 'province' ) )
    context = {'cities': cities}
    return render( request, 'order_module/cities_dropdown.html', context )


@login_required
def complete_order(request):
    open_order: Order = Order.objects.get( owner=request.user, is_paid=False )
    if open_order is None:
        return redirect( 'home_module:home-view' )
    context = {
        'title': 'complete order'
    }
    complete_form = CompleteForm( request.POST or None )
    if request.method == 'POST':
        if complete_form.is_valid():
            open_order.name = complete_form.cleaned_data.get( 'name' )
            open_order.family = complete_form.cleaned_data.get( 'family' )
            open_order.post_code = complete_form.cleaned_data.get( 'post_code' )
            open_order.phone_number = complete_form.cleaned_data.get( 'phone_number' )
            open_order.province = complete_form.cleaned_data.get( 'province' )
            open_order.city = complete_form.cleaned_data.get( 'city' )
            open_order.address = complete_form.cleaned_data.get( 'address' )
            open_order.description = complete_form.cleaned_data.get( 'description' )
            open_order.save()
            return HttpResponseRedirect( request.path_info )
    context['complete_form'] = complete_form
    return render( request, 'order_module/complete_order.html', context )


@login_required( login_url='account_module:login' )
def user_orders_view(request):
    user_orders = Order.objects.filter( owner=request.user )
    context = {
        'title': 'user orders',
        'orders': user_orders
    }
    return render( request, 'order_module/user_orders.html', context )

@login_required( login_url='account_module:login' )
def user_order_detail(request):
    pass