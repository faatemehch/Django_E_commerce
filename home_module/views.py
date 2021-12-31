from django.shortcuts import render


def home_view(request):
    context = {'title': 'home'}
    return render( request, 'home_module/home_page.html', context )


def header(request):
    context = {}
    return render( request, 'shared/header.html', context )


def footer(request):
    context = {}
    return render( request, 'shared/footer.html', context )
