from .cart import Cart

#crear context processor para que el carro funcione en toda la pag.
def cart(request):
    return{'cart': Cart(request)}