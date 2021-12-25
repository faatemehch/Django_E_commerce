from django.urls import path
from . import views

app_name = 'product_module'

urlpatterns = [
    path( '', views.ProductListView.as_view(), name='product-list' ),
    path( '<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail' ),
]
