from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Gender(models.Model):
    name = models.CharField(max_length=30)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    email = models.EmailField()
    date_birth = models.DateField()
    phone_number = models.CharField(max_length=30)
    gender = models.ForeignKey(Gender, related_name='genders', on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=255)


class CustomerAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.DecimalField(decimal_places=10, max_digits=10, default=0)
    blocked_balance = models.DecimalField(decimal_places=10, max_digits=10, default=0)


@receiver(post_save, sender=Client)
def create_student_additional_tables(sender: Client, instance: Client, created: bool, **kwargs):
    if created:
        CustomerAccount.objects.create(user=instance.user)


@receiver(post_save, sender=Client)
def save_student_additional_tables(sender: Client, instance: Client, **kwargs):
    instance.user.customeraccount.save()





