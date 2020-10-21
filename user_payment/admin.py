from django.contrib import admin
from .models import UserMoneyRequest
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.


@admin.register(UserMoneyRequest)
class UserMoneyRequestAdmin(admin.ModelAdmin):
    list_display = ('request_type', 'view_client', 'amount', 'date_created', 'accepted', 'account_number', 'build')
    list_filter = ('request_type', 'date_created', 'accepted')

    def view_client(self, obj: UserMoneyRequest):
        url = reverse(f"admin:users_client_change", args=[obj.user.client.id])

        return format_html('<a href="{}">{}</a>', url, obj.user.client)

