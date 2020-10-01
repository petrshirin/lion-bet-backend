from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from users.models import CustomerAccount
from django.utils.timezone import now
# Create your models here.


class UserMoneyRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=6, default='input')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date_created = models.DateTimeField(default=now)
    accepted = models.BooleanField(default=None, null=True)
    build = models.CharField(max_length=32, default=None, null=True)


@receiver(post_save, sender=UserMoneyRequest)
def change_user_balance(sender: UserMoneyRequest, instance: UserMoneyRequest, created: bool, **kwargs):
    if created:
        customer_account = CustomerAccount.objects.filter(user=instance.user).first()
        if instance.amount > customer_account.current_balance:
            instance.accepted = False
            instance.save()


@receiver(post_save, sender=UserMoneyRequest)
def save_student_additional_tables(sender: UserMoneyRequest, instance: UserMoneyRequest, **kwargs):
    if instance.accepted:
        customer_account = CustomerAccount.objects.filter(user=instance.user).first()
        if instance.request_type == 'input':
            customer_account.current_balance += instance.amount
        else:
            customer_account.current_balance -= instance.amount


