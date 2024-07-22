from django.shortcuts import redirect, render
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime


#transbank
import os
from django.http import HttpResponse
from transbank.common.options import WebpayOptions
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.error.transbank_error import TransbankError
from cart.cart import Cart



def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		order = Order.objects.get(id=pk)
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']

			if status == "true":
				order = Order.objects.filter(id=pk)
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				order = Order.objects.filter(id=pk)
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, 'payment/orders.html', {"order":order, "items":items})




	else:
		messages.success(request, "Access Denied")
		return redirect('home')


def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			order = Order.objects.filter(id=num)
			now = datetime.datetime.now()
			order.update(shipped=True, date_shipped=now)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			order = Order.objects.filter(id=num)
			now = datetime.datetime.now()
			order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')



def init_transaction(request):
    if request.method == 'POST':
        cart = Cart(request)

        amount = cart.cart_total()

        buy_order = "orden_compra_12345678"
        session_id = "sesion_1234564"
        return_url = "http://127.0.0.1:8000/"

        try:
            transaction = Transaction()
            response = transaction.create(buy_order, session_id, amount, return_url)
            return redirect(response['url'] + '?token_ws=' + response['token'])
        except TransbankError as e:
            return HttpResponse(str(e))
    else:
        return HttpResponse("Método no permitido.", status=405)

def transaction_response(request):
    token = request.GET.get('token_ws')
    try:
        transaction = Transaction()
        response = transaction.commit(token)
        if response['status'] == 'AUTHORIZED':
            # Procesa los datos de la transacción
            transaction_status = response['status']
            transaction_date = response['accounting_date']
            #card_number = response['card_number']
            payment_type = response['payment_type_code']
            amount = response['amount']
            #receipt = response['receipt']
            order_number = response['buy_order']
            #return HttpResponse("Transacción autorizada.")
            # Renderiza la plantilla con los datos
            return render(request, 'transaction_details.html', {
                'transaction_status': transaction_status,
                'transaction_date': transaction_date,
                #'card_number': card.card_number,
                'payment_type': payment_type,
                'amount': amount,
                #'receipt': receipt,
                'order_number': order_number
            })
        else:
            return HttpResponse("Transacción fallida.")
    except TransbankError as e:
        return HttpResponse(str(e))
###########################################


def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals
        
        
    
    
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            order_id = create_order.pk
            
            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                    
                for key,value in quantities().items():   
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()
            #Borrar carro
            for key in list(request.session.keys()):
                if key =="session_key":
                    del request.session[key]
        
            
            messages.success(request, "Orden puesta!")
            return redirect('home')
        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            order_id = create_order.pk
            
            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                    
                for key,value in quantities().items():   
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()
                        
            #Borrar carro
            for key in list(request.session.keys()):
                if key =="session_key":
                    del request.session[key]
                    
            #borrar carro de db
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart="")
            
            messages.success(request, "Orden puesta!")
            return redirect('home')
    else:
        messages.success(request, "Acceso denegado.")
        return redirect('home')



def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

        else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})


        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        messages.success(request, "Acceso denegado.")
        return redirect('home')


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        #usuario registrado
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        #usuario invitado
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})


def payment_succes(request):

    return render(request, "payment/payment_succes.html", {})


