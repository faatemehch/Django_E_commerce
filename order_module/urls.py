from django.urls import path
from . import views

app_name = 'order_module'

urlpatterns = [
    path( 'add-user-order/', views.add_user_order, name='add-new-order' ),
    path( 'user-open-order/', views.user_open_order, name='user-open-order' ),
    path( 'delete_order_item/<order_detail_id>', views.delete_order_item, name='delete-order-item' ),
]
