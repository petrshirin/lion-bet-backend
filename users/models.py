import random
import string
from django.utils.timezone import now

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
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
    activated = models.BooleanField(default=False)


class CustomerAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.DecimalField(decimal_places=10, max_digits=10, default=0)
    blocked_balance = models.DecimalField(decimal_places=10, max_digits=10, default=0)


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=255)
    text = models.TextField()
    from_email = models.EmailField(default=settings.DEFAULT_EMAIL)


class UserEmail(models.Model):
    template = models.ForeignKey(EmailTemplate, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=32)
    date_created = models.DateTimeField(default=now)
    is_view = models.BooleanField(default=False)

    def generate_code(self):
        letters = string.ascii_lowercase
        self.code = ''.join(random.choice(letters) for i in range(32))


@receiver(post_save, sender=Client)
def create_student_additional_tables(sender: Client, instance: Client, created: bool, **kwargs):
    if created:
        CustomerAccount.objects.create(user=instance.user)


@receiver(post_save, sender=Client)
def save_student_additional_tables(sender: Client, instance: Client, **kwargs):
    instance.user.customeraccount.save()





