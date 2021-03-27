from django.contrib import admin
from.models import Product, Comment, Order

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Order)
class Admin(admin.ModelAdmin):
    fields = ('product_fk', 'user_fk', 'product_count', 'cost', 'order_code', 'date_order',)
    list_display = ('product_fk', 'user_fk', 'product_count', 'cost', 'order_code', 'date_order',)
    list_filter = ('order_code', 'date_order', 'accepted',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'count', 'description')
    fields = ('name', 'price', 'count', 'description', 'image')
    inlines = [CommentInLine,]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'author', 'time_stamp')
    fields = (('fk_product', 'author'), 'comment')

admin.site.register(Comment, CommentAdmin)