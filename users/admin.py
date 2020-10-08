from django.contrib import admin
from .models import Gender, Client, CustomerAccount, EmailTemplate, UserEmail, AdminPaymentLog
# Register your models here.


admin.site.register(Gender)

admin.site.register(CustomerAccount)
admin.site.register(EmailTemplate)
admin.site.register(UserEmail)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", 'get_full_name', 'activated')
    list_filter = ('city', 'gender', 'activated')
    search_fields = ("first_name__startswith", 'second_name__startswith', 'email__startswith')

    def get_full_name(self, obj: Client):
        return f'{obj.first_name} {obj.second_name}'


@admin.register(AdminPaymentLog)
class PaymentLogAdminPanel(admin.ModelAdmin):
    list_display = ("id", 'admin', 'amount')
    list_filter = ('admin',)





