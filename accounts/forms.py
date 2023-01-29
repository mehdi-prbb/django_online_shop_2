from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from . models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']

    def save(self, commit:True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password from this <a href="../password/">link</a>'
        )

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


class UserRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    full_name = forms.CharField(label='full name', widget=forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))


    def clean_email(self):
        email = self.cleaned_data['email']
        user = CustomUser.objects.filter(email=email).exists()
        
        if user:
            raise ValidationError('This email already exist')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = CustomUser.objects.filter(phone_number=phone).exists()

        if len(phone) != 11:
            raise ValidationError('Invalid phone number')
        
        if user:
            raise ValidationError('This phone number already exist')
        return phone

    def clean(self):
        cd = super().clean()
        pass1 = cd.get('password1')
        pass2 = cd.get('password2')

        if pass1 and pass2 and len(pass1) <= 8:
            raise ValidationError("Password must be more than 8 character")

        if pass1 != pass2:
            raise ValidationError("Password Does'nt match together")

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    user_name = forms.CharField(label='email or phone:', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
