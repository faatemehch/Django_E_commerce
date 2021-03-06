"""E_commerce_application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path( '', include( 'home_module.urls', namespace='home_module' ) ),
    path( 'products/', include( 'product_module.urls', namespace='product_module' ) ),
    path( 'order/', include( 'order_module.urls', namespace='order_module' ) ),
    path( 'accounts/', include( 'account_module.urls', namespace='account_module' ) ),
    path( 'contact-us/', include( 'contact_module.urls', namespace='contact_module' ) ),
    path( 'admin/', admin.site.urls ),
]

if settings.DEBUG:
    urlpatterns += static( settings.STATIC_URL, document_root=settings.STATIC_ROOT )
    urlpatterns += static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
