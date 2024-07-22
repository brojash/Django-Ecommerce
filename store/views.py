from django.shortcuts import render, redirect
from .models import Product, Category, Profile, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
import json

from cart.cart import Cart


#################


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()

            messages.success(request, "Tu informacion se ha actualizado correctamente!")
            return redirect('home')
        return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request, "Debes estar Registrado para acceder!")
        return redirect('home')




def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Tu contrasena se ha actualizado correctamente!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})
    else:
        messages.succes(request, "Debes estar registrado para ver esta pagina!")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.succes(request, "El perfil se ha actualizado correctamente!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.succes(request, "Debes estar Registrado para acceder!")
        return redirect('home')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})

def category(request, foo):
    #remplazo guion por espacio
    foo = foo.replace('-',' ')
    #tomar categoria desde la url
    try:
        #buscar categoria
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request,("Esa categoria no existe!"))
        return redirect('home')


def product(request,pk):
        product = Product.objects.get(id=pk)
        return render(request, 'product.html', {'product':product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            #agregar carro antiguo
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request,("Has Ingresado con exito!"))
            return redirect('home')
        else:
            messages.success(request,("Ha ocurrido un error, intentalo denuevo."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,("Te has desconectado."))
    return redirect('home')

def register_user(request):
    form =SignUpForm()
    if request.method =="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("Usuario creado!, Porfavor rellena tu informacion de usuario."))
            return redirect('update_info')
        else:
            messages.success(request,("Ha ocurrido un error, intentalo denuevo."))
            return redirect('home')
    else:
        return render(request, 'register.html', {'form':form})