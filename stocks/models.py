from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models


class NewUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(("email адрес"), unique=True)
    password = models.CharField(max_length=255, verbose_name="Пароль")
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")

    USERNAME_FIELD = 'email'

    objects = NewUserManager()


class Service(models.Model):
    title = models.TextField(max_length=255, verbose_name="Название услуги")
    description = models.TextField(max_length=255, verbose_name="Описание услуги")
    url = models.CharField(max_length=255, blank=True, null=True, verbose_name="Фото услуги")
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена услуги")

    def __str__(self):
        return f'{self.title} -- {self.cost}'


class Order(models.Model):
    status = models.TextField(max_length=50, verbose_name="Статус заявки")
    created = models.DateTimeField(auto_now=True, verbose_name="Дата создания заявки")
    activated = models.DateTimeField(null=True, auto_now=False, verbose_name="Дата активации заявки")
    completed = models.DateTimeField(null=True, auto_now=False, verbose_name="Дата завершения заявки")
    creator_id = models.IntegerField(verbose_name="Создатель заявки", null=True)
    moderator_id = models.IntegerField(verbose_name="Модератор услуг", null=True)
    service = models.ManyToManyField('Service', blank=True, related_name='service', null=True)
