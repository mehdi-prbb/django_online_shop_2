from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages

from . models import Product
from .import tasks


class ProductsListView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, 'products/products_list.html', {'products':products})
    

class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'products/product_detail.html', {'product':product})
    

class BucketHome(View):
    template_name = 'products/bucket.html'

    def get(self, request):
        # age async bood
        # objects = all_bucket_object_tasks.delay()
        objects = tasks.all_bucket_object_task()
        return render(request, self.template_name, {'objects':objects})
    

class DeleteBucketObject(View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'your object will be delete soon.')
        return redirect('products:bucket')
