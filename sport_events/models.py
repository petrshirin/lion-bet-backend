from django.db import models
from random import randint


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


class Tournament(models.Model):
    api_id = models.IntegerField(verbose_name=u'Api Id')
    name = models.CharField(max_length=255, verbose_name=u'Название')
    name_en = models.CharField(max_length=255, verbose_name=u'Название на английском')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='t_sport', verbose_name=u'Спорт')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='t_country', verbose_name=u'Страна')
    request_type = models.CharField(max_length=4, default='line', verbose_name=u'Тип')
    deleted = models.BooleanField(default=False, verbose_name=u'Удален')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'


class MatchEvent(models.Model):
    oc_group_name = models.CharField(max_length=255, verbose_name=u'Название группы Рынка Коэффициентов')
    oc_name = models.CharField(max_length=255, verbose_name=u'Название исхода')
    oc_rate = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=u'Коэффициент')
    oc_pointer = models.CharField(max_length=100, verbose_name=u'Поинтер для API')
    deleted = models.BooleanField(default=False, verbose_name=u'Удален')
    admin_created = models.BooleanField(default=False, verbose_name=u'Создан админом')

    def __str__(self):
        return f'{self.oc_group_name} {self.oc_name}'

    class Meta:
        verbose_name = 'Исход'
        verbose_name_plural = 'Исходы'

    def create_oc_pointer(self):
        self.oc_pointer = f"{self.match_set.first().game_id}|0|0|0"


class Match(models.Model):
    game_num = models.IntegerField(verbose_name=u'Номер игры')
    game_id = models.IntegerField(verbose_name=u'Id')
    # uniq = models.CharField(max_length=100)
    name = models.CharField(max_length=255, verbose_name=u'Название')
    name_en = models.CharField(max_length=255, verbose_name=u'Название на английском')
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
    score_full = models.CharField(max_length=20, default='0:0', verbose_name=u'Полный счет')
    score_period = models.CharField(max_length=10, default='0:0', verbose_name=u'Счет по периодам')
    period_name = models.CharField(max_length=20, default='line', verbose_name=u'Ткущий период')
    request_type = models.CharField(max_length=4, default='line', verbose_name=u'Тип')
    deleted = models.BooleanField(default=False, verbose_name=u'Удален')
    ended = models.BooleanField(default=False, verbose_name=u'Законен')
    admin_created = models.BooleanField(default=False, verbose_name=u'Создан админом')

    def __str__(self):
        return f'{self.tournament} {self.opp_1_name}/{self.opp_2_name}'

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'
        ordering = ['deleted', '-game_start']

    def create_game_num_and_game_id(self):
        last_obj = Match.objects.filter(admin_created=True).last()
        if last_obj:
            self.game_id = last_obj.game_id - 1
            self.game_num = last_obj.game_num - 1
        else:
            self.game_id = -1
            self.game_num = -1


class MatchAdminResult(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    winner = models.CharField(choices=[('П1', 'П1'), ('П2', 'П2'), ('X', 'X')], max_length=2)
    total = models.CharField(choices=[('Б', 'Б'), ('М', 'М')], max_length=1)

    def __str__(self):
        return f'{self.match} {self.winner} {self.total}'

    class Meta:
        verbose_name = 'Результат матча, созданный админом'
        verbose_name_plural = 'Результаты матчей, созданные админом'
        ordering = ['match']

