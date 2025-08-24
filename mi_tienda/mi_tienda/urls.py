from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),
    
    # URLs de la aplicación de usuarios
    path('users/', include('users.urls', namespace='users')),
    
    # URLs de la aplicación de productos (incluye la página de inicio)
    path('', include('products.urls', namespace='products')),
    
    # URLs de la aplicación del carrito
    path('cart/', include('cart.urls', namespace='cart')),
    
    # URLs de la aplicación de pedidos
    path('orders/', include('orders.urls', namespace='orders')),
]

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personalización del admin
admin.site.site_header = "Mi Tienda - Administración"
admin.site.site_title = "Mi Tienda Admin"
admin.site.index_title = "Panel de Administración"