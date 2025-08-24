from django.db import models
from django.conf import settings
from django.utils import timezone
from products.models import Product
from decimal import Decimal
import random
import string

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente de pago'),
        ('paid', 'Pagado'),
        ('processing', 'Procesando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]
    
    PAYMENT_METHODS = [
        ('credit_card', 'Tarjeta de Crédito'),
        ('debit_card', 'Tarjeta de Débito'),
        ('paypal', 'PayPal'),
        ('cash', 'Efectivo'),
        ('transfer', 'Transferencia Bancaria'),
    ]
    
    # Relación con el usuario
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Estado del pedido
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Información de pago
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, verbose_name="Método de pago")
    payment_status = models.BooleanField(default=False, verbose_name="Estado de pago")
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de pago")
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name="ID de transacción")
    
    # Totales
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")
    iva_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="IVA total")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    
    # Información de envío
    shipping_address = models.TextField(blank=True, verbose_name="Dirección de envío")
    shipping_city = models.CharField(max_length=100, blank=True, verbose_name="Ciudad")
    shipping_zipcode = models.CharField(max_length=20, blank=True, verbose_name="Código postal")
    shipping_country = models.CharField(max_length=100, blank=True, verbose_name="País")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    notes = models.TextField(blank=True, verbose_name="Notas adicionales")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f'Pedido #{self.id} - {self.user.username}'

    def get_status_color(self):
        colors = {
            'pending': 'bg-yellow-100 text-yellow-800',
            'paid': 'bg-blue-100 text-blue-800',
            'processing': 'bg-purple-100 text-purple-800',
            'shipped': 'bg-indigo-100 text-indigo-800',
            'delivered': 'bg-green-100 text-green-800',
            'cancelled': 'bg-red-100 text-red-800',
        }
        return colors.get(self.status, 'bg-gray-100 text-gray-800')

    def generate_transaction_id(self):
        """Genera un ID de transacción único"""
        if not self.transaction_id:
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.transaction_id = f'TX-{timestamp}-{random_str}'
        return self.transaction_id

    def mark_as_paid(self, payment_method):
        """Marca el pedido como pagado"""
        self.status = 'paid'
        self.payment_status = True
        self.payment_method = payment_method
        self.payment_date = timezone.now()
        self.generate_transaction_id()
        self.save()

    def get_payment_status_display(self):
        """Texto descriptivo del estado de pago"""
        return "Pagado" if self.payment_status else "Pendiente"

    @property
    def items_count(self):
        """Cantidad total de items en el pedido"""
        return sum(item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Pedido")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    
    # Precios al momento de la compra (para mantener historial)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio con IVA")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio sin IVA")
    iva_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Porcentaje de IVA")
    
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    class Meta:
        verbose_name = "Item del pedido"
        verbose_name_plural = "Items del pedido"
        unique_together = ['order', 'product']

    def __str__(self):
        return f'{self.quantity} x {self.product.name} (Orden #{self.order.id})'

    @property
    def get_cost(self):
        """Costo total del item (precio con IVA * cantidad)"""
        return self.price * self.quantity
        
    @property
    def get_subtotal(self):
        """Subtotal del item (precio sin IVA * cantidad)"""
        return self.unit_price * self.quantity
        
    @property
    def get_iva_amount(self):
        """Monto de IVA del item"""
        return (self.unit_price * self.iva_percentage / 100) * self.quantity

    def save(self, *args, **kwargs):
        """Auto-calcular precios si no están establecidos"""
        if not self.price and self.product:
            self.price = self.product.price_with_iva
        if not self.unit_price and self.product:
            self.unit_price = self.product.unit_price
        if not self.iva_percentage and self.product:
            self.iva_percentage = self.product.iva_percentage
        super().save(*args, **kwargs)