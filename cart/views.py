from django.shortcuts import render, get_object_or_404

from .cart import Cart

from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):

    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})

def cart_add(request):
    #obtener carro
    cart = Cart(request)
    #probar POST
    if request.POST.get('action') == 'post':
        #obtener cosas
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        #ver productos en db
        product = get_object_or_404(Product, id=product_id)
        #guardar en la sesion
        cart.add(product=product, quantity=product_qty)
        #cantidad del carrito
        cart_quantity = cart.__len__()
        #dar una respuesta
        #response = JsonResponse({'Product name: ':product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request,("Producto agregado al carrito !"))
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #obtener cosas
        product_id = int(request.POST.get('product_id'))
        #call delete fn
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request,("Producto eliminado !"))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #obtener cosas
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request,("Tu carrito ha sido actualizado !"))
        return response
        #return redirect('cart_summary')

