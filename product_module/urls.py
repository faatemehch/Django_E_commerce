from django.urls import path
from . import views

app_name = 'product_module'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('new-products/', views.NewProductListView.as_view(), name='new-product-list'),
    path('product-brand/<brand_name>/', views.ProductByBrand.as_view(), name='product-list-by-brand'),
    path('product-category/<category_name>/', views.ProductByCategory.as_view(), name='product-list-by-category'),
    path('product-ajax-price/', views.get_product_detail, name='product-detail-price'),
    path('search/', views.product_list_by_search, name='search-products-list'),
    path('ajax_filtering/', views.get_json_filtering, name='ajax_filtering')
]
