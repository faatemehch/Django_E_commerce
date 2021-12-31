from django.shortcuts import render
from .models import Slider
from product_module.models import Product, Brand


def home_view(request):
    context = {'title': 'home',
               'sliders': Slider.objects.all(),
               'new_products': Product.objects.all()
               }
    return render( request, 'home_module/home_page.html', context )


def header(request):
    context = {
        'brands': Brand.objects.all()
    }
    return render( request, 'shared/header.html', context )


def footer(request):
    context = {}
    return render( request, 'shared/footer.html', context )
