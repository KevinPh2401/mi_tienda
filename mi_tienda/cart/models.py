# El carrito se manejará con sesiones, no necesitamos modelos específicos
# Pero podríamos agregar un modelo para persistir carritos si fuera necesario
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.conf import settings


class Cart(models.Model):
    """Modelo opcional para persistir carritos en base de datos"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"

class CartItem(models.Model):
    """Items del carrito persistente"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.product.price_with_iva * self.quantity