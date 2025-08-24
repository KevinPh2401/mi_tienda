from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
import random
import string
from .models import Order, OrderItem
from cart.cart import Cart
from .forms import OrderCreateForm

@login_required
def order_create(request):
    cart = Cart(request)
    
    if not cart:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            
            # Calcular totales
            subtotal = Decimal('0.00')
            total_iva = Decimal('0.00')
            
            for item in cart:
                item_subtotal = item['product'].unit_price * item['quantity']
                item_iva = item['product'].iva_amount * item['quantity']
                subtotal += item_subtotal
                total_iva += item_iva
            
            order.subtotal = subtotal
            order.iva_total = total_iva
            order.total = subtotal + total_iva
            order.save()
            
            # Crear items del pedido
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price_with_iva,
                    unit_price=item['product'].unit_price,
                    iva_percentage=item['product'].iva_percentage
                )
            
            request.session['order_id'] = order.id
            return redirect('orders:payment_method')
    else:
        # Prellenar con datos del usuario si existen
        initial_data = {}
        if request.user.first_name and request.user.last_name:
            initial_data['first_name'] = request.user.first_name
            initial_data['last_name'] = request.user.last_name
        if request.user.email:
            initial_data['email'] = request.user.email
        
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'form': form
    })

@login_required
def payment_method(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('cart:cart_detail')
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        order.payment_method = payment_method
        order.save()
        return redirect('orders:payment_process')
    
    return render(request, 'orders/payment_method.html', {'order': order})

@login_required
def payment_process(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('cart:cart_detail')
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Simulación de procesamiento de pago
    if request.method == 'POST':
        # Generar ID de transacción simulado
        transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        
        # Actualizar orden
        order.payment_status = True
        order.payment_date = timezone.now()
        order.status = 'paid'
        order.transaction_id = transaction_id
        order.save()
        
        # Limpiar carrito
        cart = Cart(request)
        cart.clear()
        
        # Eliminar order_id de la sesión
        if 'order_id' in request.session:
            del request.session['order_id']
        
        messages.success(request, f'¡Pago realizado exitosamente! ID de transacción: {transaction_id}')
        return redirect('orders:order_detail', order_id=order.id)
    
    return render(request, 'orders/payment_process.html', {'order': order})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})