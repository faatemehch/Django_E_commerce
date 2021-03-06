from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template, render_to_string
from django.views.generic import ListView, DetailView
from .models import Order, OrderDetail, Coupon, City
from product_module.models import Product
from django.http import JsonResponse, HttpResponse
from .forms import CompleteForm
import random
import string


def create_tracking_code():
    # create tracking code
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


@login_required
def add_user_order(request):
    if request.method == 'GET':
        return redirect('home_module:home-view')
    order_form_data = request.POST  # get form info (POST request)
    # get product order details
    product: Product = Product.objects.filter(id=order_form_data['product']).first()
    product_detail = product.productdetail_set.filter(color=order_form_data['product-color']).first()
    # find or create an open order
    order: Order = Order.objects.filter(owner=request.user, is_paid=False).first()
    if order is None:
        tracking_code = create_tracking_code()
        order: Order = Order.objects.create(owner=request.user,
                                            tracking_code=tracking_code)
    order_detail: OrderDetail = order.orderdetail_set.filter(product=product, product_detail=product_detail).first()
    if order_detail is None:
        order_detail = order.orderdetail_set.create(product=product, product_detail=product_detail,
                                                    count=order_form_data['quantity'])
    else:
        order_detail.count += int(order_form_data['quantity'])

    if product_detail.discount_price:
        order_detail.price = product_detail.discount_price
    else:
        order_detail.price = product_detail.price
    product_detail.quantity -= int(order_form_data['quantity'])
    product_detail.save()
    order_detail.save()
    return redirect('order_module:user-open-order')


class UserOpenOrder(DetailView, LoginRequiredMixin):
    model = Order
    template_name = 'order_module/user_open_order_list.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        open_order = Order.objects.filter(owner=self.request.user, is_paid=False).first()
        return open_order

    def get_context_data(self, **kwargs):
        context = super(UserOpenOrder, self).get_context_data()
        context['title'] = f'{self.request.user.username} open order'
        return context


@login_required
def change_item_count(request):
    print(request)
    '''
           delete, decrease or increase counter of an order detail
    '''
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({'status': 'detail_or_state_not_found', 'icon': 'warning'})
    detail: OrderDetail = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                     order__owner_id=request.user.id).first()
    if detail is None:
        return JsonResponse({'status': 'detail_found', 'icon': 'warning'})
    if state == 'increase':
        if detail.product_detail.quantity > 0:
            detail.count += 1
            detail.save()
            detail.product_detail.quantity -= 1
            detail.product_detail.save()
        else:
            return JsonResponse({'status': 'the required number is not available', 'icon': 'warning'})
    elif state == 'decrease':
        if detail.count == 1:
            detail.delete()
        else:
            detail.count -= 1
            detail.save()
            detail.product_detail.quantity += 1
            detail.product_detail.save()
    elif state == 'all':
        detail.product_detail.quantity += detail.count
        detail.product_detail.save()
        detail.delete()
    else:
        return JsonResponse({'status': 'invalid_state', 'icon': 'error'})
    return JsonResponse({'success': 'successful',
                         'icon': 'success',
                         'body': render_to_string(
                             template_name='order_module/includes/open_order_detail_component.html',
                             context={'order': Order.objects.filter(owner_id=request.user.id, is_paid=False).first()})
                         })


@login_required
def add_coupon_code(request):
    open_order: Order = Order.objects.filter(owner=request.user, is_paid=False).first()
    if open_order is not None:
        if open_order.coupon_code is None:
            coupon_form = request.POST['coupon']
            coupon = Coupon.objects.filter(code=coupon_form).first()
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
    return JsonResponse(context)


def get_cities(request, ):
    cities = City.objects.filter(province_id=request.GET.get('province'))
    context = {'cities': cities}
    return render(request, 'order_module/cities_dropdown.html', context)


@login_required
def complete_order(request):
    open_order: Order = Order.objects.get(owner=request.user, is_paid=False)
    if open_order is None:
        return redirect('home_module:home-view')
    context = {
        'title': 'complete order'
    }
    complete_form = CompleteForm(request.POST or None, instance=open_order)
    if request.method == 'POST':
        if complete_form.is_valid():
            open_order.name = complete_form.cleaned_data.get('name')
            open_order.family = complete_form.cleaned_data.get('family')
            open_order.post_code = complete_form.cleaned_data.get('post_code')
            open_order.phone_number = complete_form.cleaned_data.get('phone_number')
            open_order.province = complete_form.cleaned_data.get('province')
            open_order.city = complete_form.cleaned_data.get('city')
            open_order.address = complete_form.cleaned_data.get('address')
            open_order.description = complete_form.cleaned_data.get('description')
            open_order.save()
            return redirect('order_module:order-detail', open_order.id)
    context['complete_form'] = complete_form
    return render(request, 'order_module/complete_order.html', context)


@login_required(login_url='account_module:login')
def user_orders_view(request):
    user_orders = Order.objects.filter(owner=request.user)
    context = {
        'title': 'user orders',
        'orders': user_orders
    }
    return render(request, 'order_module/user_orders.html', context)


@login_required(login_url='account_module:login')
def user_order_detail(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    context = {'title': 'order detail', 'order': order}
    return render(request, 'order_module/order_detail.html', context)


# export an order as a pdf
def export_pdf_order(request, order_id):
    response = HttpResponse(content_type='appllication/pdf')
    order = Order.objects.filter(id=order_id).first()
    response['content-Disposiotion'] = 'filename=order' + '.pdf'
    template_path = 'order_module/html_to_pdf_order.html'
    template = get_template(template_path)
    context = {'order': order}
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)
    return response
