from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    additional_info = models.TextField(
        blank=True, 
        verbose_name="Información adicional",
        help_text="Talla, peso, características especiales"
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name="Imagen"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Precio unitario"
    )
    iva_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('19.00'),
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))],
        verbose_name="IVA (%)"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Categoría"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def iva_amount(self):
        """Calcula el monto del IVA"""
        return (self.unit_price * self.iva_percentage / 100).quantize(Decimal('0.01'))

    @property
    def price_with_iva(self):
        """Calcula el precio con IVA incluido"""
        return (self.unit_price + self.iva_amount).quantize(Decimal('0.01'))

    def get_image_url(self):
        if self.image:
            return self.image.url
        return '/static/images/no-image.png'