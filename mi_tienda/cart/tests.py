from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product, Category
from cart.models import Cart, CartItem
from decimal import Decimal

User = get_user_model()

class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kevin", password="123456")
        self.category = Category.objects.create(name="Calzado")
        self.product = Product.objects.create(
            name="Adidas Running",
            description="Zapatillas de running",
            additional_info="Talla 43",
            unit_price=Decimal('300000.00'),
            iva_percentage=Decimal('19.00'),
            stock=20,
            category=self.category
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_add_item_to_cart(self):
        self.assertEqual(self.cart.items.count(), 1)
        self.assertEqual(self.cart_item.quantity, 2)

    def test_update_quantity(self):
        self.cart_item.quantity = 5
        self.cart_item.save()
        total = self.cart_item.quantity * self.product.price_with_iva
        self.assertEqual(total, Decimal('1785000.00'))

    def test_remove_item(self):
        self.cart_item.delete()
        self.assertEqual(self.cart.items.count(), 0)
