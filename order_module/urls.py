from django.urls import path
from . import views

app_name = 'order_module'

urlpatterns = [
    path('', views.add_user_order, name='add-new-order')
]
