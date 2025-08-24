from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
@login_required
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
        messages.success(request, f'Producto "{product.name}" agregado al carrito')
        return redirect('cart:cart_detail')
    
    messages.error(request, 'Error al agregar el producto al carrito')
    return redirect('products:product_detail', pk=product_id)

@require_POST
@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'Producto "{product.name}" eliminado del carrito')
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request):
    cart = Cart(request)
    
    # Inicializar totales
    subtotal = Decimal('0.00')
    total_iva = Decimal('0.00')
    valid_items = []
    
    # Filtrar solo items válidos
    for item in cart:
        if hasattr(item, 'product') and hasattr(item.product, 'unit_price'):
            product = item.product
            quantity = item.quantity
            
            # Calcular valores
            item_subtotal = product.unit_price * quantity
            item_iva = product.iva_amount * quantity
            
            # Agregar información al item
            item.unit_price = product.unit_price
            item.iva_amount = product.iva_amount
            item.subtotal = item_subtotal
            item.iva_total = item_iva
            
            # Acumular totales
            subtotal += item_subtotal
            total_iva += item_iva
            
            valid_items.append(item)
    
    total = subtotal + total_iva
    
    context = {
        'cart': valid_items,  # Usar solo items válidos
        'subtotal': subtotal,
        'total_iva': total_iva,
        'total': total,
        'cart_total_items': len(valid_items),
    }
    return render(request, 'cart/detail.html', context)

@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Carrito vaciado correctamente')
    return redirect('cart:cart_detail')

from django.http import JsonResponse

@require_POST
@login_required
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
        
        # Responder diferente para AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Producto "{product.name}" agregado al carrito',
                'cart_total_items': cart.get_total_items()
            })
        
        messages.success(request, f'Producto "{product.name}" agregado al carrito')
        return redirect('cart:cart_detail')
    
    # Para requests AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'message': 'Error al agregar el producto'
        })
    
    messages.error(request, 'Error al agregar el producto al carrito')
    return redirect('products:product_detail', pk=product_id)