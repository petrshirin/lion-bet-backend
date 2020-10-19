from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from users.models import CustomerAccount
from django.utils.timezone import now
# Create your models here.


class UserMoneyRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'Пользователь')
    request_type = models.CharField(max_length=6, default='input', verbose_name=u'Тип пополнения')
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=u'Сумма')
    date_created = models.DateTimeField(default=now, verbose_name=u'Дата создания')
    accepted = models.BooleanField(default=None, null=True, verbose_name=u'Одобрена')
    build = models.CharField(max_length=32, default=None, null=True, verbose_name=u'Код для пополнения')
    method = models.CharField(max_length=50, default='input_qiwi', null=True)

    def __str__(self):
        return f'{self.request_type} {self.amount}'

    class Meta:
        verbose_name = 'Запрос на Ввод/Вывод'
        verbose_name_plural = 'Запросы на Ввод/Вывод'


@receiver(post_save, sender=UserMoneyRequest)
def check_user_balance(sender: UserMoneyRequest, instance: UserMoneyRequest, created: bool, **kwargs):
    if created:
        if instance.request_type == 'output':
            customer_account = CustomerAccount.objects.filter(user=instance.user).first()
            if instance.amount > customer_account.current_balance:
                instance.accepted = False
                instance.save()


@receiver(post_save, sender=UserMoneyRequest)
def change_user_balance(sender: UserMoneyRequest, instance: UserMoneyRequest, **kwargs):
    if instance.accepted:
        customer_account = CustomerAccount.objects.filter(user=instance.user).first()
        if instance.request_type == 'input':
            customer_account.current_balance += instance.amount
        else:
            customer_account.current_balance -= instance.amount

        customer_account.save()


