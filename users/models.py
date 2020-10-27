import random
import string
from django.utils.timezone import now

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.urls import reverse


# Create your models here.
class Gender(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'Пол')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Гендер'
        verbose_name_plural = 'Гендеры'


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=u'Пользователь')
    first_name = models.CharField(max_length=255, verbose_name=u'Имя')
    second_name = models.CharField(max_length=255, verbose_name=u'Фамилия')
    email = models.EmailField(verbose_name=u'Почта')
    date_birth = models.DateField(verbose_name=u'Дата рождения')
    phone_number = models.CharField(max_length=30, verbose_name=u'Телефон')
    gender = models.ForeignKey(Gender, related_name='genders', on_delete=models.SET_NULL, null=True, verbose_name=u'Пол')
    city = models.CharField(max_length=255, verbose_name=u'Город')
    activated = models.BooleanField(default=False, verbose_name=u'Активированный')
    date_register = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.pk}. {self.first_name} {self.second_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class CustomerAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=u'Пользователь')
    current_balance = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name=u'Текущий баланс')
    blocked_balance = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name=u'Заблокированный баланс')
    blocked = models.BooleanField(default=False, verbose_name=u'Счет заблокирован')

    def __str__(self):
        return f"{self.user.client.first_name} {self.user.client.second_name}"

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=255, verbose_name=u'Тема')
    text = models.TextField(verbose_name=u'Текст')
    from_email = models.CharField(default=settings.DEFAULT_EMAIL, verbose_name=u'Отправитель', max_length=100)

    class Meta:
        verbose_name = 'Шаблон для Email'
        verbose_name_plural = 'Шаблоны для Email'


class UserEmail(models.Model):
    template = models.ForeignKey(EmailTemplate, on_delete=models.PROTECT, verbose_name=u'Шаблон')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'Пользователь')
    code = models.CharField(max_length=32, verbose_name=u'Код для интерактивных писем')
    date_created = models.DateTimeField(default=now, verbose_name=u'Дата отправки')
    is_view = models.BooleanField(default=False, verbose_name=u'Активировано')

    def generate_code(self):
        letters = string.ascii_lowercase
        self.code = ''.join(random.choice(letters) for i in range(32))

    class Meta:
        verbose_name = 'Письмо пользователю'
        verbose_name_plural = 'Письма пользователям'


class AdminPaymentLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(default=now)

    def get_url_for_user(self):
        if self.user:
            return reverse('admin:users_customeraccount_change', args=[self.user.customeraccount.id])
        else:
            return ''

    def get_url_for_admin(self):
        if self.admin:
            return reverse('admin:auth_user_change', args=[self.admin.id])
        else:
            return ''


@receiver(post_save, sender=Client)
def create_student_additional_tables(sender: Client, instance: Client, created: bool, **kwargs):
    if created:
        CustomerAccount.objects.create(user=instance.user)


@receiver(post_save, sender=Client)
def save_student_additional_tables(sender: Client, instance: Client, **kwargs):
    instance.user.customeraccount.save()






