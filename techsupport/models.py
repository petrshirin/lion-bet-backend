from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Имя')
    email = models.EmailField(verbose_name=u'Email')

    def __str__(self):
        return f'{self.pk}. {self.name}'

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


def create_new_number():
    last_request = ClientRequest.objects.last()
    if last_request:
        return last_request.number + 1
    else:
        return 1000


class ClientRequest(models.Model):
    number = models.IntegerField(default=create_new_number, verbose_name=u'Номер')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name=u'Департамент')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'Пользователь')
    request = models.TextField(verbose_name=u'Текст')
    email_to_answer = models.EmailField(verbose_name=u'Email для ответа')
    closed = models.BooleanField(default=False, verbose_name=u'Закрыт')

    class Meta:
        verbose_name = 'Запрос Пользователя'
        verbose_name_plural = 'Запросы Пользователей'









