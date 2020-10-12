from django.contrib import admin
from .models import Department, ClientRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse

# Register your models here.

admin.site.register(Department)


@admin.register(ClientRequest)
class ClientRequestAdmin(admin.ModelAdmin):
    list_display = ("number", "department", "view_client", 'request', 'closed')
    list_filter = ("closed", 'department', 'user__client')

    def view_client(self, obj: ClientRequest):
        url = reverse(f"admin:users_client_change", args=[obj.user.client.id])

        return format_html('<a href="{}">{}</a>', url, obj.user.client)

    view_client.short_description = "Клиент"
