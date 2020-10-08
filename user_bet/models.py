from django.db import models
from users.models import CustomerAccount, User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from sport_events.models import MatchEvent, Match


class UserBet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'Пользователь')
    bet_type = models.CharField(max_length=8, verbose_name=u'Тип ставки')
    bet_code = models.CharField(max_length=32, unique=True, verbose_name=u'Код')
    events = models.ManyToManyField(MatchEvent, verbose_name=u'Исходы')
    win_coefficient = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=u'Коэффицент победы')
    user_bet = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Ставка пользователя')
    user_win = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Возможный выигрыш')
    is_went = models.BooleanField(default=None, null=True, verbose_name=u'Выиграна')
    date_created = models.DateTimeField(default=now, verbose_name=u'Дата создания')
    deleted = models.BooleanField(default=False, verbose_name=u'Удалена')

    def __str__(self):
        return f'{self.user.client.id} {self.bet_type} {self.win_coefficient}'

    class Meta:
        verbose_name = 'Ставка пользователя'
        verbose_name_plural = 'Ставки пользователей'




