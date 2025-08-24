from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product, Category
from orders.models import Order, OrderItem
from decimal import Decimal

User = get_user_model()

class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kevin", password="123456")
        self.category = Category.objects.create(name="Calzado")
        self.product = Product.objects.create(
            name="New Balance",
            description="Calzado cómodo",
            additional_info="Talla 42",
            unit_price=Decimal('200000.00'),
            iva_percentage=Decimal('19.00'),
            stock=5,
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,
            subtotal=Decimal('0'),
            iva_total=Decimal('0'),
            total=Decimal('0')
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=self.product.price_with_iva,
            unit_price=self.product.unit_price,
            iva_percentage=self.product.iva_percentage
        )

    def test_order_creation(self):
        self.assertEqual(self.order.items.count(), 1)
        self.assertEqual(self.order_item.quantity, 2)

    def test_order_total_calculation(self):
        total = sum(item.total_price for item in [self.order_item])
        self.assertEqual(total, self.order_item.price * self.order_item.quantity)
