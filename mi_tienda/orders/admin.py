from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['get_cost', 'get_subtotal', 'get_iva_amount']

    def get_cost(self, obj):
        return f"${obj.get_cost:,.2f}"
    get_cost.short_description = 'Total con IVA'

    def get_subtotal(self, obj):
        return f"${obj.get_subtotal:,.2f}"
    get_subtotal.short_description = 'Subtotal'

    def get_iva_amount(self, obj):
        return f"${obj.get_iva_amount:,.2f}"
    get_iva_amount.short_description = 'IVA'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_payment_status_display', 'status', 'total', 'created_at', 'payment_method']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at', 'payment_date']
    search_fields = ['user__username', 'user__email', 'transaction_id', 'shipping_address']
    readonly_fields = ['created_at', 'updated_at', 'transaction_id', 'get_payment_status_display']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('user', 'status', 'created_at', 'updated_at')
        }),
        ('Información de Pago', {
            'fields': ('payment_status', 'get_payment_status_display', 'payment_method', 'payment_date', 'transaction_id')
        }),
        ('Totales', {
            'fields': ('subtotal', 'iva_total', 'total')
        }),
        ('Información de Envío', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_zipcode', 'shipping_country', 'phone_number', 'notes')
        }),
    )

    def get_payment_status_display(self, obj):
        return "Pagado" if obj.payment_status else "Pendiente"
    get_payment_status_display.short_description = 'Estado de Pago'

    def save_model(self, request, obj, form, change):
        """Generar ID de transacción automáticamente si se marca como pagado"""
        if obj.payment_status and not obj.transaction_id:
            obj.generate_transaction_id()
        super().save_model(request, obj, form, change)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'unit_price', 'iva_percentage', 'get_cost']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['product__name', 'order__user__username', 'order__transaction_id']
    readonly_fields = ['get_cost', 'get_subtotal', 'get_iva_amount']
    
    def get_cost(self, obj):
        return f"${obj.get_cost:,.2f}"
    get_cost.short_description = 'Total con IVA'

    def get_subtotal(self, obj):
        return f"${obj.get_subtotal:,.2f}"
    get_subtotal.short_description = 'Subtotal'

    def get_iva_amount(self, obj):
        return f"${obj.get_iva_amount:,.2f}"
    get_iva_amount.short_description = 'IVA'