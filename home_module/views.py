from django.shortcuts import render


def header(request):
    context = {}
    return render( request, 'shared/header.html', context )


def footer(request):
    context = {}
    return render( request, 'shared/footer.html', context )
