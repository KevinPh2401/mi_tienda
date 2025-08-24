from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        """Inicializar el carrito"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Agregar un producto al carrito o actualizar su cantidad"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price_with_iva)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Marcar la sesión como modificada"""
        self.session.modified = True

    def remove(self, product):
        """Remover un producto del carrito"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterar sobre los items del carrito y obtener los productos desde la BD"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Contar todos los items en el carrito"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calcular el precio total del carrito"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_items(self):
        """Obtener cantidad total de items"""
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """Vaciar el carrito"""
        del self.session[settings.CART_SESSION_ID]
        self.save()