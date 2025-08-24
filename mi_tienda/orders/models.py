from django.db import models
from django.conf import settings  # Importar settings
from products.models import Product
from decimal import Decimal

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]
    
    # Cambiar User por settings.AUTH_USER_MODEL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Información del pedido
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva_total = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Información de entrega (opcional)
    shipping_address = models.TextField(blank=True, verbose_name="Dirección de envío")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    notes = models.TextField(blank=True, verbose_name="Notas adicionales")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f'Pedido {self.id} - {self.user.username}'

    def get_status_color(self):
        colors = {
            'pending': 'bg-yellow-100 text-yellow-800',
            'processing': 'bg-blue-100 text-blue-800',
            'shipped': 'bg-purple-100 text-purple-800',
            'delivered': 'bg-green-100 text-green-800',
            'cancelled': 'bg-red-100 text-red-800',
        }
        return colors.get(self.status, 'bg-gray-100 text-gray-800')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio al momento de la compra
    quantity = models.PositiveIntegerField(default=1)
    
    # Información de IVA al momento de la compra
    iva_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio sin IVA

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def get_cost(self):
        return self.price * self.quantity
        
    @property
    def get_subtotal(self):
        return self.unit_price * self.quantity
        
    @property
    def get_iva_amount(self):
        return (self.unit_price * self.iva_percentage / 100) * self.quantity