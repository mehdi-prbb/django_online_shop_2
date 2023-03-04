from django.urls import path

from . import views


app_name = 'orders'


urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('apply_coupon/<int:order_id>/', views.ApplyCouponView.as_view(), name='apply_coupon'),
]
