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
    build = models.CharField(max_length=32, default=None, null=True, verbose_name=u'Код для пополнения', blank=True)
    method = models.CharField(max_length=50, default='input_qiwi', null=True, blank=True)
    account_number = models.CharField(max_length=50, default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.request_type} {self.amount}'

    def get_hidden_account_number(self):
        if self.account_number:
            if len(self.account_number) > 15:
                return ''.join(self.account_number[:4] + ''.join(['*' for i in range(len(self.account_number) - 8)]) + self.account_number[-4:])
            elif len(self.account_number) > 4:
                return ''.join(['*' for i in range(len(self.account_number) - 4)]) + self.account_number[-4:]
            else:
                return self.account_number
        return ''

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
            amount_to_add = _double_first_pay(float(instance.amount), instance.user)
            customer_account.current_balance = float(customer_account.current_balance) + amount_to_add
        else:
            customer_account.current_balance = float(customer_account.current_balance) - float(instance.amount)

        customer_account.save()


def _double_first_pay(amount: float, user: User):
    if UserMoneyRequest.objects.filter(user=user, request_type='input', accepted=True).count() == 1:
        return amount * 2
    else:
        return amount