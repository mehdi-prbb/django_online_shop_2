from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import datetime

from . models import Order, OrderItem, Coupon
from cart.cart import Cart
from . forms import CouponApplyForm



class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        form = self.form_class
        return render(request, 'orders/order.html', {'order':order, 'form':form})
    

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
    

class ApplyCouponView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)

        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now,
                                            valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'this code does not exist.')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail', order_id)




