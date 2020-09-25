from django.contrib import admin
from .models import Gender, Client, CustomerAccount, EmailTemplate, UserEmail
# Register your models here.


admin.site.register(Gender)
admin.site.register(Client)
admin.site.register(CustomerAccount)
admin.site.register(EmailTemplate)
admin.site.register(UserEmail)
