from django.urls import path
from . import views

app_name = 'order_module'

urlpatterns = [
    path('add-user-order/', views.add_user_order, name='add-new-order'),
    path('add-coupon-code/', views.add_coupon_code, name='add-coupon-code'),
    path('user-orders/', views.user_orders_view, name='user-orders'),
    path('order-detail/<order_id>', views.user_order_detail, name='order-detail'),
    path('complete-order/', views.complete_order, name='complete-order'),
    path('user-open-order/', views.UserOpenOrder.as_view(), name='user-open-order'),
    path('change_item_counter', views.change_item_count, name='change_item_counter'),
    path('ajax/load-cities/', views.get_cities, name='load_cities'),
    path('export-pdf/<int:order_id>/', views.export_pdf_order, name='export-pdf-order')
]
