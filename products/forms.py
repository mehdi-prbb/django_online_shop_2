from django import forms


class UploadImageForm(forms.Form):
    image = forms.ImageField()


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10)