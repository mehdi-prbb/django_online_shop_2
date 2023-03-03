from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import json
import requests

from orders.models import Order


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id' : order.id,
        }
        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_total_price(),
        "Description": settings.description,
        "Phone": request.user.phone_number,
        "CallbackURL": settings.CallbackURL,
    }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data,headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return {'status': True, 'url': settings.ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response
    
        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}
        

class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request, authority):
        order_id = request.session['order_pay']['order-id']
        order = Order.objects.get(id=int(order_id))

        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_total_price(),
        "Authority": authority,
    }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(settings.ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                order.is_paid = True
                order.save()
                return {'status': True, 'RefID': response['RefID']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

