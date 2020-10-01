from django.db import models
from users.models import CustomerAccount, User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from sport_events.models import MatchEvent, Match


class UserBet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bet_type = models.CharField(max_length=8)
    bet_code = models.CharField(max_length=32, unique=True)
    events = models.ManyToManyField(MatchEvent)
    win_coefficient = models.DecimalField(max_digits=6, decimal_places=3)
    user_bet = models.DecimalField(max_digits=10, decimal_places=2)
    user_win = models.DecimalField(max_digits=10, decimal_places=2)
    is_went = models.BooleanField(default=None, null=True)
    date_created = models.DateTimeField(default=now)
    deleted = models.BooleanField(default=False)




