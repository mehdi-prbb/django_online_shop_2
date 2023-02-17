from django.shortcuts import render, get_object_or_404
from django.views import View

from . models import Product
from .task import all_bucket_object_tasks


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
        # age sync bood
        # objects = all_bucket_object_tasks.delay()
        objects = all_bucket_object_tasks()
        print('='*90)
        print(objects)
        return render(request, self.template_name, {'objects':objects})
