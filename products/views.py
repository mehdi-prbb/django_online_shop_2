import os
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages

from . models import Product
from . import tasks
from . forms import UploadImageForm



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
    

class DownloadBucketObject(View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your download will be start soon.')
        return redirect('products:bucket')


class UploadBucketObject(View):
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