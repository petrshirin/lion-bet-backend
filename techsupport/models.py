from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()


def create_new_number():
    last_request = ClientRequest.objects.last()
    if last_request:
        return last_request.number + 1
    else:
        return 1000


class ClientRequest(models.Model):
    number = models.IntegerField(default=create_new_number)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.TextField()
    email_to_answer = models.EmailField()
    closed = models.BooleanField(default=False)









