from django.db import models


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        managed = False
        db_table = 'auth_user'


class Service(models.Model):
    title = models.TextField(max_length=255, verbose_name="Название услуги")
    description = models.TextField(max_length=255, verbose_name="Описание услуги")
    url = models.CharField(max_length=255, blank=True, null=True, verbose_name="Фото услуги")
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена услуги")

    def __str__(self):
        return f'{self.title} -- {self.cost}'


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    status = models.TextField(max_length=50, verbose_name="Статус заявки")
    created = models.DateTimeField(auto_now=True, verbose_name="Дата создания заявки")
    activated = models.DateTimeField(null=True, auto_now=False, verbose_name="Дата активации заявки")
    completed = models.DateTimeField(null=True, auto_now=False, verbose_name="Дата завершения заявки")
    creator_id = models.IntegerField(verbose_name="Создатель заявки")
    moderator_id = models.IntegerField(verbose_name="Модератор услуг")

# class OrderEvent(models.Model):
#     order_id = models.ForeignKey('Order', on_delete=models.DO_NOTHING, verbose_name="Идентификатор заявки"),
#     service_id = models.ForeignKey('Service', on_delete=models.DO_NOTHING, verbose_name="Идентификатор Услуги"),
#
#     class Meta:
#         managed = False
#         db_table = 'order_event'
