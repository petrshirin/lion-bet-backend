from django.contrib import admin
from django.forms import ModelForm

from .models import *
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from ajax_select import make_ajax_form


# Register your models here.

admin.site.register(MatchEvent)


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('api_id', 'name', 'deleted')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('api_id', 'name', 'sport', 'deleted')
    list_filter = ('sport', 'deleted')


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('api_id', 'name', 'sport', 'deleted')
    list_filter = ('sport', 'deleted')


class AdminMatchForm(ModelForm):
    class Meta:
        model = Match
        fields = "__all__"

    events = AutoCompleteSelectMultipleField('ajax_events', required=False, help_text="Press + and add new event")


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('game_num', 'name', 'sport', 'tournament', 'game_start', 'admin_created', 'deleted')
    list_filter = ('sport', 'deleted', 'game_start', 'admin_created')
    search_fields = ('opp_1_name__startswith', 'opp_2_name__startswith', 'name__startswith', 'sport__name__startswith', 'game_id')
    ordering = ['deleted', '-game_start']
    form = AdminMatchForm


@admin.register(MatchAdminResult)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('match', 'winner', 'total')
    list_filter = ('match', 'winner', 'total')
    search_fields = ('match__name__startswith', 'sport__name__startswith')
