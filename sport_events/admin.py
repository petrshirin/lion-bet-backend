from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Sport)
admin.site.register(Country)
admin.site.register(Tournament)
admin.site.register(Match)
admin.site.register(MatchEvent)
