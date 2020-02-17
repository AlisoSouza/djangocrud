from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm

# Create your views here.
def list_products(request):
    products = Product.objects.all()
    context = {
    'products':products,
    }
    return render(request, 'products.html',context)
def create_products(request):
    form = ProductForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('list_products')
    return render(request,'products-form.html',context)
def update_product(request,id):
    product = Product.objects.get(id=id)
    form = ProductForm(request.POST or None, instance=product)
    context = {
    'product': product,'form':form    }
    if form.is_valid():
        form.save()
        return redirect('list_products')
    return render(request,'products-form.html',context)
def delete_product(request,id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    if request.method == 'POST':
        product.delete()
        return redirect('list_products')
    return render(request,'prod-delete-confirm.html',context)
