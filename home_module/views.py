from django.shortcuts import render
from django.views.generic.base import View
from .models import Slider
from product_module.models import Product, Brand, Category


class HomeView(View):
    def get(self, request):
        context = {'title': 'home',
                   'sliders': Slider.objects.all(),
                   'new_products': Product.objects.all()
                   }
        return render(request, 'home_module/home_page.html', context)


def header(request):
    context = {
        'brands': Brand.objects.all()
    }
    return render(request, 'shared/header.html', context)


def footer(request):
    context = {'brands': Brand.objects.all(), 'categories': Category.objects.all()}
    return render(request, 'shared/footer.html', context)
