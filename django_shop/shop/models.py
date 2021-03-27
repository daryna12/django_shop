from django.db import models
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

fs = FileSystemStorage(location='/media/img')

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name = 'Название продукта' )
    price = models.FloatField(verbose_name = 'Стоимость продукта')
    count = models.IntegerField(verbose_name = 'Количество продукта')
    description = models.TextField(verbose_name = 'Описание продукта')
    image = models.ImageField(max_length=100, verbose_name ='Изображение продукта', 
                                                upload_to='img', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse("product_url", kwargs={"product_id": self.pk})
    
    def get_update_url(self):
        return reverse("update_product_url", kwargs={"product_id": self.pk})
        
    def get_delete_url(self):
        return reverse("delete_product_url", kwargs={"product_id": self.pk})

class Comment(models.Model):
    comment = models.TextField(verbose_name='Текст комментария')
    author = models.CharField( verbose_name='Автор комментария',max_length=200)
    time_stamp = models.DateTimeField(auto_now=True, verbose_name='Дата комментария')
    fk_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name = 'comments')
    class Meta:
        verbose_name ="Комментарий"
        verbose_name_plural ="Комментарии"

    def __str__(self):
        return self.author

    # def get_absolute_url(self):
    #     return reverse("product_url", kwargs={"product_id": self.pk})
class Order(models.Model):
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                            verbose_name = 'Продукт')
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Пользователь')
    product_count = models.IntegerField(verbose_name = 'Количество')
    cost = models.FloatField(verbose_name = 'Сумма')
    order_code = models.CharField(max_length=20, verbose_name = 'Код заказа', blank=True, null=True)
    date_order = models.DateTimeField(auto_now=True, 
                                        verbose_name = 'Время и дата заказа')
    accepted = models.BooleanField(verbose_name='Статус заказа', default=False)

    def __str__(self):
        return '{}'.formft(self.date_order)

