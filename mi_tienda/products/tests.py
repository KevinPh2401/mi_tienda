from django.test import TestCase
from products.models import Product, Category
from decimal import Decimal

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Calzado")
        self.product = Product.objects.create(
            name="Zapatillas Nike",
            description="Zapatillas deportivas",
            additional_info="Talla 42, color negro",
            unit_price=Decimal('250000.00'),
            iva_percentage=Decimal('19.00'),
            stock=10,
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Zapatillas Nike")
        self.assertEqual(self.product.unit_price, Decimal('250000.00'))
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(self.product.category.name, "Calzado")

    def test_price_with_iva(self):
        expected = self.product.unit_price + (self.product.unit_price * self.product.iva_percentage / 100)
        self.assertEqual(self.product.price_with_iva, expected.quantize(Decimal('0.01')))
