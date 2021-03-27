from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index_url' ),
    path('products/', product_list, name = 'product_list_url'),
    path('products/<int:product_id>', product_detail, name = 'product_url'),
    path('products/<int:product_id>/update', Product_UPdate.as_view(),
                                                name = 'update_product_url'),
    path('products/add', Product_Create.as_view(), name = 'add_product_url'),
    path('products/<int:product_id>/delete', Product_Delite.as_view(),
                                                name = 'delete_product_url'),
    path('comment/<int:product_id>', add_comment, name='add_comment_url'),
    path('order/<int:product_id>', order_product ,name = 'add_order_url'),
    path('profile/', Profile_Update.as_view(), name='profile_url'),
    path('order/<int:product_id>', order_product ,name = 'add_order_url'),
    path('profile/cart', cart_read, name = 'cart_url'),
    path('profile/cart/order', cart_order, name = 'cart_order_url'),
    path('profile/cart/ordered', ordered_list, name = 'ordered_list_url'),
    path('profile/cart/<str:order_code>', read_ordered , name = 'ordered_url'),
]