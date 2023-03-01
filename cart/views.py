from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .cart import Cart
from .forms import CartAddForm
from products.models import Product


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart.html', {'cart':cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('cart:cart')
