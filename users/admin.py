from django.contrib import admin
from .models import Gender, Client, CustomerAccount
# Register your models here.


admin.site.register(Gender)
admin.site.register(Client)
admin.site.register(CustomerAccount)
