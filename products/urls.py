from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='products_list'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
