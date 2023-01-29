from django.shortcuts import render, redirect
from django.views import View
import random
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate, login

from . forms import UserRegisterForm, VerifyCodeForm, UserLoginForm
from utils import send_otp_code, cal_seconds
from . models import OtpCode, CustomUser


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('pages:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            random_code = random.randint(1000, 9999)

            otp = OtpCode.objects.filter(phone_number=form.cleaned_data['phone'])
            if otp.exists():
                messages.error(request, 'We have already sent you a otp code')
            else:
                OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
                send_otp_code(form.cleaned_data['phone'], random_code)

                request.session['user_registration_info'] = {
                    'phone_number' : form.cleaned_data['phone'],
                    'email' : form.cleaned_data['email'],
                    'full_name' : form.cleaned_data['full_name'],
                    'password' : form.cleaned_data['password1']
                }
                messages.success(request, 'code sent you by text message')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form':form})


class VerifyCodeView(View):
    form_class = VerifyCodeForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('pages:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form':form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        
        created_time = cal_seconds(str(code_instance.created.time()))
        now_time = cal_seconds(str(datetime.now().time()))
        check_expiration = now_time - created_time

        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            if check_expiration > 120:
                code_instance.delete()
                messages.error(request, 'code expired')
                return redirect('accounts:verify_code')

            elif cd['code'] == code_instance.code:
                CustomUser.objects.create_user(user_session['phone_number'], user_session['email'],
                                                user_session['full_name'], user_session['password'])
                code_instance.delete()
                messages.success(request, 'you registerd successfully')
                return redirect('pages:home')
            else:
                messages.error(request, 'Invalide code')
                return redirect('accounts:verify_code')
        return redirect('pages:home')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('pages:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you are logged in successfully')
                if self.next:
                    return redirect(self.next)
                return redirect('pages:home')
            messages.error(request, 'Invalid username or password')
        
        return render(request, self.template_name, {'form':form})