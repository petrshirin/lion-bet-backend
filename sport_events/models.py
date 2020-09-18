from django.db import models


# Create your models here.
class Sport(models.Model):
    api_id = models.IntegerField()
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)


class Country(models.Model):
    api_id = models.IntegerField()
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)


class Tournament(models.Model):
    api_id = models.IntegerField()
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='t_sport')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='t_country')


class MatchEvent(models.Model):
    oc_group_name = models.CharField(max_length=255)
    oc_name = models.CharField(max_length=255)
    oc_rate = models.DecimalField(max_digits=9, decimal_places=5)
    oc_pointer = models.CharField(max_length=100)


class Match(models.Model):
    game_num = models.IntegerField()
    uniq = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    game_start = models.DateTimeField()
    opp_1_name = models.CharField(max_length=255)
    opp_2_name = models.CharField(max_length=255)
    opp_1_id = models.IntegerField()
    opp_2_id = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='m_tournament')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='m_sport')
    events = models.ManyToManyField(MatchEvent)

