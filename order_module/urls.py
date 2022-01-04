from django.urls import path
from . import views

app_name = 'order_module'

urlpatterns = [
    path( 'add-user-order/', views.add_user_order, name='add-new-order' ),
    path( 'user-open-order/', views.user_open_order, name='user-open-order' )
]
