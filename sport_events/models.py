from django.db import models
from random import randint

from django.db.models import Q
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
import string
import random


# Create your models here.
class Sport(models.Model):
    api_id = models.IntegerField(verbose_name=u'Api Id')
    name = models.CharField(max_length=255, verbose_name=u'Название')
    name_en = models.CharField(max_length=255, verbose_name=u'Название на английском')
    deleted = models.BooleanField(default=False, verbose_name=u'Удалена')
    request_type = models.CharField(max_length=4, default='line', verbose_name=u'Тип')

    def __str__(self):
        return f'{self.pk} {self.name} ({self.api_id})'

    class Meta:
        verbose_name = 'Вид Спорта'
        verbose_name_plural = 'Виды Спорта'


class Country(models.Model):
    api_id = models.IntegerField(verbose_name=u'Api Id')
    name = models.CharField(max_length=255, verbose_name=u'Название')
    name_en = models.CharField(max_length=255, verbose_name=u'Название на английском')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name=u'Спорт')
    deleted = models.BooleanField(default=False, verbose_name=u'Удалена')
    request_type = models.CharField(max_length=4, default='line', verbose_name=u'Тип')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


def create_random_str():
    pass


class Tournament(models.Model):
    api_id = models.IntegerField(verbose_name=u'Api Id', blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=u'Название')
    name_en = models.CharField(max_length=255, verbose_name=u'Название на английском')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='t_sport', verbose_name=u'Спорт')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='t_country', verbose_name=u'Страна')
    request_type = models.CharField(max_length=4, default='line', verbose_name=u'Тип')
    admin_created = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False, verbose_name=u'Удален')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'
        ordering = ['-admin_created']

    def create_api_id(self):
        last_obj = Tournament.objects.filter(admin_created=True).all()
        if len(last_obj) >= 2:
            last_obj = last_obj[len(last_obj) - 2]
        else:
            last_obj = None
        if last_obj:
            if last_obj.api_id:
                self.api_id = -1
            else:
                last_obj.api_id = -1
        else:
            self.api_id = -1


class MatchEvent(models.Model):
    oc_group_name = models.CharField(max_length=255, verbose_name=u'Название группы Рынка Коэффициентов')
    oc_name = models.CharField(max_length=255, verbose_name=u'Название исхода')
    oc_rate = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=u'Коэффициент')
    oc_pointer = models.CharField(max_length=100, verbose_name=u'Поинтер для API', blank=True)
    short_name = models.CharField(max_length=15, default=None, null=True)
    deleted = models.BooleanField(default=False, verbose_name=u'Удален')
    admin_created = models.BooleanField(default=False, verbose_name=u'Создан админом')
    last_changed = models.SmallIntegerField(default=0, verbose_name='Последнее изменение')

    def __str__(self):
        return f'{self.oc_group_name} {self.oc_name}'

    class Meta:
        verbose_name = 'Исход'
        verbose_name_plural = 'Исходы'

    def create_oc_pointer(self):
        self.oc_pointer = f"{self.match_set.first().game_id if self.match_set.first() else ''}|0|0|0"


def create_default_uniq():
    last_obj = Match.objects.filter(admin_created=True).order_by('pk').all()
    if len(last_obj) >= 1:
        last_obj = last_obj[len(last_obj) - 1]
    else:
        last_obj = None
    if last_obj:
        return str(int(last_obj.uniq) - 1) if last_obj.uniq else -1
    else:
        return str(-1)


def create_random_uniq():
    pass



def create_default_game_id():
    last_obj = Match.objects.filter(admin_created=True).order_by('pk').all()
    if len(last_obj) >= 1:
        last_obj = last_obj[len(last_obj) - 1]
    else:
        last_obj = None
    if last_obj:
        return last_obj.game_id - 1 if last_obj.game_id else -1
    else:
        return -1


def create_default_game_num():
    last_obj = Match.objects.filter(admin_created=True).order_by('pk').all()
    if len(last_obj) >= 1:
        last_obj = last_obj[len(last_obj) - 1]
    else:
        last_obj = None
    if last_obj:
        return last_obj.game_num - 1 if last_obj.game_num else -1
    else:
        return -1


class Match(models.Model):
    game_num = models.IntegerField(verbose_name=u'Номер игры', null=True, blank=True, default=create_default_game_num)
    game_id = models.IntegerField(verbose_name=u'Id', null=True, blank=True, default=create_default_game_id)
    uniq = models.CharField(max_length=100, null=True, unique=True, blank=True, default=create_default_uniq)
    name = models.CharField(max_length=255, verbose_name=u'Название', blank=True, null=True)
    name_en = models.CharField(max_length=255, verbose_name=u'Название на английском', blank=True, null=True)
    game_start = models.DateTimeField(verbose_name=u'Дата начала')
    opp_1_name = models.CharField(max_length=255, verbose_name=u'Команда 1')
    opp_2_name = models.CharField(max_length=255, verbose_name=u'Комадна 2')
    opp_1_id = models.IntegerField(null=True, default=None, verbose_name=u'Id Комадны 1')
    opp_2_id = models.IntegerField(null=True, default=None, verbose_name=u'Id Команды 2')
    opp_1_icon = models.URLField(default=None, null=True, verbose_name=u'Ссылка на иконку 1')
    opp_2_icon = models.URLField(default=None, null=True, verbose_name=u'Ссылка на иконку 2')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches', verbose_name=u'Турнир')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='m_sport', verbose_name=u'Спорт')
    events = models.ManyToManyField(MatchEvent, verbose_name=u'Исходы')
    score_full = models.CharField(max_length=50, default='0:0', verbose_name=u'Полный счет')
    score_period = models.CharField(max_length=50, default='0:0', verbose_name=u'Счет по периодам')
    period_name = models.CharField(max_length=50, default='line', verbose_name=u'Текущий период')
    request_type = models.CharField(max_length=4, default='line', verbose_name=u'Тип')
    deleted = models.BooleanField(default=False, verbose_name=u'Удален')
    ended = models.BooleanField(default=False, verbose_name=u'Законен')
    admin_created = models.BooleanField(default=False, verbose_name=u'Создан админом')

    def __str__(self):
        return f'{self.tournament} {self.opp_1_name}/{self.opp_2_name}'

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'
        ordering = ['-game_start']
        constraints = [
            models.UniqueConstraint(fields=['game_id'], condition=Q(ended=False), name='uniq_game_id')
        ]

    def create_game_num_game_id_and_uniq(self):
        last_obj = Match.objects.filter(admin_created=True).order_by('pk').all()
        if len(last_obj) >= 2:
            last_obj = last_obj[len(last_obj) - 1]
        else:
            last_obj = None
        if last_obj:
            print(last_obj.game_id)
            self.game_id = last_obj.game_id - 1 if last_obj.game_id else -1
            self.game_num = last_obj.game_num - 1 if last_obj.game_num else -1
            self.uniq = str(int(last_obj.uniq) - 1) if last_obj.uniq else str(-1)
        else:
            self.game_id = -1
            self.game_num = -1
            self.uniq = str(-1)


class MatchAdminResult(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    winner = models.CharField(choices=[('П1', 'П1'), ('П2', 'П2'), ('X', 'X')],
                              max_length=2, verbose_name=u'Победитель')
    total = models.CharField(choices=[('Б', 'Б'), ('М', 'М')], max_length=1, blank=True, default=None, null=True)
    total_score = models.CharField(max_length=10, verbose_name=u'Точный счет')
    date_closed = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return f'{self.match} {self.winner} {self.total}'

    class Meta:
        verbose_name = 'Результат матча, созданный админом'
        verbose_name_plural = 'Результаты матчей, созданные админом'
        ordering = ['match']


#@receiver(post_save, sender=Match)
#def create_admin_match(sender: Match, instance: Match, created: bool, **kwargs):
#    if created:
#        if instance.admin_created:
#            instance.create_game_num_game_id_and_uniq()
#            instance.save()


@receiver(post_save, sender=MatchEvent)
def create_admin_match_event(sender: MatchEvent, instance: MatchEvent, created: bool, **kwargs):
    if created:
        if instance.admin_created:
            instance.create_oc_pointer()
            instance.save()


@receiver(post_save, sender=Tournament)
def create_admin_tournament(sender: Tournament, instance: Tournament, created: bool, **kwargs):
    if created:
        if instance.admin_created:
            instance.create_api_id()
            instance.save()

