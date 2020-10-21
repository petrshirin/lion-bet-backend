from django.contrib import admin
from .models import UserMoneyRequest

# Register your models here.


@admin.register(UserMoneyRequest)
class UserMoneyRequestAdmin(admin.ModelAdmin):
    list_display = ('request_type', 'amount', 'date_created', 'accepted', 'account_number', 'build')
    list_filter = ('request_type', 'date_created', 'accepted')

