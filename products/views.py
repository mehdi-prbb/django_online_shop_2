import os
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages

from . models import Product, Category
from . import tasks
from . forms import UploadImageForm, CartAddForm
from utils import IsAdminUserMixin



class ProductsListView(View):
    def get(self, request, cat_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if cat_slug:
            category = Category.objects.get(slug=cat_slug)
            products = products.filter(category=category)
        return render(request, 'products/products_list.html', {'products':products, 'categories':categories})
    

class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(request, 'products/product_detail.html', {'product':product, 'form':form})
    

class BucketHome(IsAdminUserMixin, View):
    template_name = 'products/bucket.html'

    def get(self, request):
        # age async bood
        # objects = all_bucket_object_tasks.delay()
        objects = tasks.all_bucket_object_task()
        return render(request, self.template_name, {'objects':objects})
    

class DeleteBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'your object will be delete soon.')
        return redirect('products:bucket')
    

class DownloadBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your download will be start soon.')
        return redirect('products:bucket')


class UploadBucketObject(IsAdminUserMixin, View):
    form_class = UploadImageForm

    def get(self, request):
        form = self.form_class
        return render(request, 'products/bucket_add.html', {'form':form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            key = form.cleaned_data['image']
            print(str(key))
            tasks.upload_object_task.delay(str(key))
            messages.success(request, 'your upload will be start soon.')
            return redirect('products:bucket')
        return render(request, 'products/bucket_add.html', {'form':form})