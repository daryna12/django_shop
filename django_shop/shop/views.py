from django.shortcuts import render, redirect, reverse
from .models import Product, Comment, Order
from .forms import *
from  django.views.generic import View
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum


def index(request):
    return render(request, 'shop/index.html')

def product_list(request):
    products_obj = Product.objects.all()
    context_obj = {'products': products_obj}
    return render(request, 'shop/products.html', context=context_obj)

def product_detail(request, product_id):
    product = Product.objects.get(id = product_id)
    context_obj = {'product': product}
    if request.user.is_authenticated:
        context_obj['form']= CommentForm
        context_obj['form_order'] = OrderForm
    return render(request, 'shop/product_detail.html', context=context_obj)

@login_required
def order_product(request,product_id):
    form = OrderForm(request.POST)
    product = Product.objects.get(id = product_id)
    user = User.objects.get(id = request.user.id)

    if form.is_valid():
        try:
            cart_product = Order.objects.get(user_fk = request.user.id, accepted = False, product_fk = product_id)
        except:
            cart_product = ''
        if cart_product:
            cart_product.product_count += form.cleaned_data['count']
            cart_product.save()
        else:  
            order = Order()
            order.product_fk = product
            order.user_fk = user
            order.product_count = form.cleaned_data['count']
            order.cost = product.price * order.product_count
            order.save()
    return redirect(product.get_absolute_url())

def cart_read(request):
    cart = Order.objects.filter(user_fk = request.user.id, accepted = False)
    sum_cost = Order.objects.filter(user_fk = request.user.id, accepted = False).aggregate(Sum('cost'))
    return render(request, 'shop/cart.html', context = {'cart':cart, 'sum_cost':sum_cost})

import string, random

letters_digits = string.ascii_uppercase + string.digits

def random_code_gen():
    random_code = ''.join(random.choice(letters_digits) for i in range(20))
    return random_code

def cart_order(request):
    cart = Order.objects.filter(user_fk = request.user.id, accepted = False)
    random_code = random_code_gen()
    for order in cart:
        order.order_code = random_code
        order.accepted = True
        order.save()
    return redirect('cart_url')

def ordered_list(request):
    ordered = Order.objects.filter(user_fk = request.user.id, accepted = True).order_by('-date_order')[:5]# .distinct('order_code')
    return render(request, 'shop/ordered_list.html', context = {'ordered': ordered})

def read_ordered(request, order_code):
    ordered = Order.objects.filter(user_fk = request.user.id, order_code = order_code)
    sum_cost = Order.objects.filter(user_fk = request.user.id, 
        order_code = order_code).aggregate(Sum('cost'))
    return render(request, 'shop/cart.html', context={'cart':ordered, 'sum_cost': sum_cost})


@login_required
def add_comment(request, product_id):
    form = CommentForm(request.POST)
    product = Product.objects.get(pk = product_id)
    if form.is_valid():
        comment = Comment()
        comment.fk_product = product
        comment.author = request.user
        comment.comment = form.cleaned_data['comment']
        comment.save()
    return redirect(product.get_absolute_url())

class Product_Create( PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = 'shop.add_product'
    def get(self, request, *args, **kwargs):
        form = ProductForm
        return render(request, 'shop/product_add.html', 
                                    context={'form':form})

    def post(self, request, *args, **kwargs):
        bound_form = ProductForm(request.POST, request.FILES)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, 'shop/product_add.html', 
                                    context={'form' :bound_form})
class Product_UPdate(PermissionRequiredMixin, View):
    permission_required = 'shop.update_product'
    def get(self, request, product_id, *args, **kwargs):
        data_obj = Product.objects.get(pk = product_id)
        form = ProductForm(instance=data_obj)
        return render(request, 'shop/product_update.html', 
                                context={'form':form, 'obj':data_obj})
    
    def post(self, request, product_id, *args, **kwargs):
        data_obj = Product.objects.get(pk = product_id)
        bound_form = ProductForm(request.POST, request.FILES, instance=data_obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()  
            return redirect(new_obj)
        return render(request, 'shop/product_update.html',
                                 context={'form':bound_form, 'obj':data_obj})
class Product_Delite(View):
    permission_required = 'shop.delete_product'
    def get(self, request, product_id, *args, **kwargs):
        data_obj = Product.objects.get(pk = product_id)
        return render(request, 'shop/product_delete.html', 
                                context={'obj':data_obj})
    def post(self, request, product_id, *args, **kwargs):
        data_obj = Product.objects.get(pk = product_id)
        data_obj.delete()
        return redirect(reverse('product_list_url'))

class Profile_Update( View): 
    def get(self, request):
        data_obj = User.objects.get(pk = request.user.id)
        form = UserUpdateForm(instance=data_obj)
        return render(request, 'shop/profile.html', 
                                context={'form':form, 'obj':data_obj})
    
    def post(self, request):
        data_obj = User.objects.get(pk = request.user.id)
        bound_form = UserUpdateForm(request.POST, instance=data_obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()  
            return redirect(to = 'shop/profile_url')
        return render(request, 'shop/profile.html',
                                 context={'form':bound_form, 'obj':data_obj})