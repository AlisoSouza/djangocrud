from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm,AccountAuthenticationForm,AccountUpdateForm
from django.template import RequestContext
from django.contrib.auth import login,authenticate,logout
from .forms import RegistrationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
# Create your views here.
@csrf_protect
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email,password=raw_password)
            login(request,account)
            return redirect('list_products')
        else:
            context['registration_form'] = form
    else: #get request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html',context)

@csrf_protect
#@login_required(redirect_field_name='login')
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
    'product': product,'form':form }
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
def logout_view(request):
    logout(request)
    return redirect('list_products')



def login_view(request):

    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('list_products')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)

            if user:
                login(request,user)
                return redirect('list_products')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request,'login.html',context)
def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST,instance = request.user)
        if form.is_valid():
            form.save()
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,

            }

        )
    context['account_form'] = form
    return render(request,'account.html',context)
