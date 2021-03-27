from django import forms
from .models import Product, Comment
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'count', 'description','image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}), 
            'price': forms.NumberInput(attrs={'class': 'form-control'}), 
            'count': forms.NumberInput(attrs={'class': 'form-control'}), 
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }



class CommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class':'form-control'
    }))

class OrderForm(forms.Form):
    count = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly':''})
        }