from django.contrib import admin
from .models import UserBet
from django.urls import reverse
from django.utils.html import format_html
from ajax_select import make_ajax_form
from sport_events.models import MatchEvent

# Register your models here.


@admin.register(UserBet)
class UserBetAdmin(admin.ModelAdmin):
    list_display = ('id', 'view_client', 'bet_type', 'user_bet', 'is_went', 'date_created', 'deleted')
    list_filter = ('user__client', 'bet_type', 'is_went', 'date_created', 'deleted')
    form = make_ajax_form(UserBet, {
        "events": "ajax_events"
    })

    def view_client(self, obj: UserBet):
        url = reverse(f"admin:users_client_change", args=[obj.user.client.id])

        return format_html('<a href="{}">{}</a>', url, obj.user.client)



