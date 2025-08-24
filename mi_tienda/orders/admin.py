from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['get_cost']

    def get_cost(self, obj):
        return f"${obj.get_cost:,.2f}"
    get_cost.short_description = 'Total'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Información del pedido', {
            'fields': ('user', 'status', 'created_at', 'updated_at')
        }),
        ('Totales', {
            'fields': ('subtotal', 'iva_total', 'total')
        }),
        ('Información de entrega', {
            'fields': ('shipping_address', 'phone_number', 'notes')
        })
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_cost']
    list_filter = ['order__created_at']
    search_fields = ['product__name', 'order__user__username']
    
    def get_cost(self, obj):
        return f"${obj.get_cost:,.2f}"
    get_cost.short_description = 'Total'