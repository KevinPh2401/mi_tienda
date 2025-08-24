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
    
    # Calcular totales
    subtotal = Decimal('0.00')
    total_iva = Decimal('0.00')
    
    for item in cart:
        product = item['product']
        quantity = item['quantity']
        item_subtotal = product.unit_price * quantity
        item_iva = product.iva_amount * quantity
        
        subtotal += item_subtotal
        total_iva += item_iva
        
        # Agregar información de IVA al item
        item['unit_price'] = product.unit_price
        item['iva_amount'] = product.iva_amount
        item['subtotal'] = item_subtotal
        item['iva_total'] = item_iva
    
    total = subtotal + total_iva
    
    context = {
        'cart': cart,
        'subtotal': subtotal,
        'total_iva': total_iva,
        'total': total,
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Carrito vacío')
    return redirect('cart:cart_detail')