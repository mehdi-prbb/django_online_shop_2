from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from . models import Order, OrderItem
from cart.cart import Cart



class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order':order})
    

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)

        for item in cart:
            OrderItem.objects.create(order=order, product=item['product_obj'],
                                     price=item['product_obj'].price,
                                     quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order.id)
