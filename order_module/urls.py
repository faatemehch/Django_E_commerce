from django.urls import path
from . import views

app_name = 'order_module'

urlpatterns = [
    path('add-user-order/', views.add_user_order, name='add-new-order'),
    path('add-coupon-code/', views.add_coupon_code, name='add-coupon-code'),
    path('user-orders/', views.user_orders_view, name='user-orders'),
    path('order-detail/<order_id>', views.user_order_detail, name='order-detail'),
    path('complete-order/', views.complete_order, name='complete-order'),
    # path( 'user-open-order/', views.user_open_order, name='user-open-order' ),
    path('user-open-order/', views.UserOpenOrder.as_view(), name='user-open-order'),
    path('delete_order_item/<order_detail_id>', views.delete_order_item, name='delete-order-item'),
    path('decrease_item_counter/<order_detail_id>', views.decrease_item_counter, name='decrease-item-counter'),
    path('increase_item_counter/<order_detail_id>', views.increase_item_counter, name='increase-item-counter'),
    path('ajax/load-cities/', views.get_cities, name='load_cities'),
]
