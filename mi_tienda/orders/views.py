from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm
from decimal import Decimal

@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, 'Tu carrito está vacío')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Calcular totales del carrito
            subtotal = Decimal('0.00')
            total_iva = Decimal('0.00')
            
            # Crear el pedido
            order = form.save(commit=False)
            order.user = request.user
            
            # Calcular totales antes de guardar
            for item in cart:
                product = item['product']
                quantity = item['quantity']
                subtotal += product.unit_price * quantity
                total_iva += product.iva_amount * quantity
            
            order.subtotal = subtotal
            order.iva_total = total_iva
            order.total = subtotal + total_iva
            order.save()
            
            # Crear los items del pedido
            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price_with_iva,
                    quantity=item['quantity'],
                    iva_percentage=product.iva_percentage,
                    unit_price=product.unit_price
                )
            
            # Limpiar el carrito
            cart.clear()
            
            messages.success(request, f'¡Pedido #{order.id} creado exitosamente!')
            return redirect('orders:order_detail', order_id=order.id)
    else:
        form = OrderCreateForm()
    
    # Calcular totales para mostrar en el formulario
    subtotal = Decimal('0.00')
    total_iva = Decimal('0.00')
    
    for item in cart:
        product = item['product']
        quantity = item['quantity']
        subtotal += product.unit_price * quantity
        total_iva += product.iva_amount * quantity
    
    total = subtotal + total_iva
    
    context = {
        'cart': cart,
        'form': form,
        'subtotal': subtotal,
        'total_iva': total_iva,
        'total': total,
    }
    return render(request, 'orders/order_create.html', context)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'orders/order_list.html', {'page_obj': page_obj})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status in ['pending', 'processing']:
        if request.method == 'POST':
            order.status = 'cancelled'
            order.save()
            messages.success(request, f'Pedido #{order.id} cancelado exitosamente')
            return redirect('orders:order_detail', order_id=order.id)
        
        return render(request, 'orders/order_cancel.html', {'order': order})
    else:
        messages.error(request, 'No se puede cancelar este pedido')
        return redirect('orders:order_detail', order_id=order.id)