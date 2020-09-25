from django.db import models


# Create your models here.
class Sport(models.Model):
    api_id = models.IntegerField()
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)
    request_type = models.CharField(max_length=4, default='line')

    def __str__(self):
        return f'{self.pk} {self.name} ({self.api_id})'


class Country(models.Model):
    api_id = models.IntegerField()
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    request_type = models.CharField(max_length=4, default='line')


class Tournament(models.Model):
    api_id = models.IntegerField()
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='t_sport')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='t_country')
    request_type = models.CharField(max_length=4, default='line')
    deleted = models.BooleanField(default=False)


class MatchEvent(models.Model):
    oc_group_name = models.CharField(max_length=255)
    oc_name = models.CharField(max_length=255)
    oc_rate = models.DecimalField(max_digits=9, decimal_places=5)
    oc_pointer = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)


class Match(models.Model):
    game_num = models.IntegerField()
    game_id = models.IntegerField()
    # uniq = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    game_start = models.DateTimeField()
    opp_1_name = models.CharField(max_length=255)
    opp_2_name = models.CharField(max_length=255)
    opp_1_id = models.IntegerField()
    opp_2_id = models.IntegerField()
    opp_1_icon = models.URLField()
    opp_2_icon = models.URLField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='m_sport')
    events = models.ManyToManyField(MatchEvent)
    score_full = models.CharField(max_length=20)
    score_period = models.CharField(max_length=10)
    period_name = models.CharField(max_length=20)
    request_type = models.CharField(max_length=4, default='line')
    deleted = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)


