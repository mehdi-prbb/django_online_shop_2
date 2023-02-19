from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='products_list'),
    path('bucket/', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj_bucket/<str:key>', views.DeleteBucketObject.as_view(), name='bucket_obj_delete'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
