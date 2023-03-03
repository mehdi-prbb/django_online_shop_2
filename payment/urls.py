from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/', views.OrderVerifyView.as_view(), name='order_verify'),
]
