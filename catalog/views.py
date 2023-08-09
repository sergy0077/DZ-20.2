from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    return render(request, 'catalog/contacts.html')


# def product_detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     return render(request, 'catalog/product_detail.html', {'product': product})


def product_detail(request, product_id):
    print(f"product_id: {product_id}")
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        print("Product does not exist")
        raise Http404("Product does not exist")
    print(f"Product name: {product.name}")
    return render(request, 'catalog/product_detail.html', {'product': product})
