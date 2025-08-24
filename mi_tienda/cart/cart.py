from decimal import Decimal
from django.conf import settings
from products.models import Product

class CartItem:
    """Clase para representar un item del carrito de forma más robusta"""
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = price * quantity

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price_with_iva),
                'product_id': product_id,
                'product_name': product.name
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterador que devuelve objetos CartItem en lugar de diccionarios"""
        product_ids = list(self.cart.keys())
        
        # Obtener productos existentes
        products = Product.objects.filter(
            id__in=product_ids, 
            is_active=True
        )
        
        product_dict = {str(p.id): p for p in products}
        
        # Crear items válidos
        for product_id, item_data in self.cart.items():
            if product_id in product_dict:
                try:
                    product = product_dict[product_id]
                    quantity = int(item_data['quantity'])
                    price = Decimal(item_data['price'])
                    
                    yield CartItem(
                        product=product,
                        quantity=quantity,
                        price=price
                    )
                except (KeyError, ValueError, TypeError):
                    # Ignorar items corruptos
                    continue

    def __len__(self):
        return sum(1 for _ in self)

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self:
            total += item.total_price
        return total

    def get_total_items(self):
        return sum(item.quantity for item in self)

    def clear(self):
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()

