# Generated by Django 3.1.1 on 2020-10-07 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport_events', '0014_auto_20201008_0006'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name': 'Матч', 'verbose_name_plural': 'Матчи'},
        ),
        migrations.AlterModelOptions(
            name='matchevent',
            options={'verbose_name': 'Исход', 'verbose_name_plural': 'Исходы'},
        ),
        migrations.AlterModelOptions(
            name='sport',
            options={'verbose_name': 'Вид Спорта', 'verbose_name_plural': 'Виды Спорта'},
        ),
        migrations.AlterModelOptions(
            name='tournament',
            options={'verbose_name': 'Турнир', 'verbose_name_plural': 'Турниры'},
        ),
        migrations.AlterField(
            model_name='country',
            name='api_id',
            field=models.IntegerField(verbose_name='Api Id'),
        ),
        migrations.AlterField(
            model_name='country',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удалена'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name_en',
            field=models.CharField(max_length=255, verbose_name='Название на английском'),
        ),
        migrations.AlterField(
            model_name='country',
            name='request_type',
            field=models.CharField(default='line', max_length=4, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='country',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport_events.sport', verbose_name='Спорт'),
        ),
        migrations.AlterField(
            model_name='match',
            name='admin_created',
            field=models.BooleanField(default=False, verbose_name='Создан админом'),
        ),
        migrations.AlterField(
            model_name='match',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удален'),
        ),
        migrations.AlterField(
            model_name='match',
            name='ended',
            field=models.BooleanField(default=False, verbose_name='Законен'),
        ),
        migrations.AlterField(
            model_name='match',
            name='events',
            field=models.ManyToManyField(to='sport_events.MatchEvent', verbose_name='Исходы'),
        ),
        migrations.AlterField(
            model_name='match',
            name='game_id',
            field=models.IntegerField(verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='match',
            name='game_num',
            field=models.IntegerField(verbose_name='Номер игры'),
        ),
        migrations.AlterField(
            model_name='match',
            name='game_start',
            field=models.DateTimeField(verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='match',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='match',
            name='name_en',
            field=models.CharField(max_length=255, verbose_name='Название на английском'),
        ),
        migrations.AlterField(
            model_name='match',
            name='opp_1_icon',
            field=models.URLField(default=None, null=True, verbose_name='Ссылка на иконку 1'),
        ),
        migrations.AlterField(
            model_name='match',
            name='opp_1_id',
            field=models.IntegerField(default=None, null=True, verbose_name='Id Комадны 1'),
        ),
        migrations.AlterField(
            model_name='match',
            name='opp_1_name',
            field=models.CharField(max_length=255, verbose_name='Команда 1'),
        ),
        migrations.AlterField(
            model_name='match',
            name='opp_2_icon',
            field=models.URLField(default=None, null=True, verbose_name='Ссылка на иконку 2'),
        ),
        migrations.AlterField(
            model_name='match',
            name='opp_2_id',
            field=models.IntegerField(default=None, null=True, verbose_name='Id Команды 2'),
        ),
        migrations.AlterField(
            model_name='match',
            name='opp_2_name',
            field=models.CharField(max_length=255, verbose_name='Комадна 2'),
        ),
        migrations.AlterField(
            model_name='match',
            name='period_name',
            field=models.CharField(default='line', max_length=20, verbose_name='Ткущий период'),
        ),
        migrations.AlterField(
            model_name='match',
            name='request_type',
            field=models.CharField(default='line', max_length=4, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='match',
            name='score_full',
            field=models.CharField(default='0:0', max_length=20, verbose_name='Полный счет'),
        ),
        migrations.AlterField(
            model_name='match',
            name='score_period',
            field=models.CharField(default='0:0', max_length=10, verbose_name='Счет по периодам'),
        ),
        migrations.AlterField(
            model_name='match',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m_sport', to='sport_events.sport', verbose_name='Спорт'),
        ),
        migrations.AlterField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='sport_events.tournament', verbose_name='Турнир'),
        ),
        migrations.AlterField(
            model_name='matchevent',
            name='admin_created',
            field=models.BooleanField(default=False, verbose_name='Создан админом'),
        ),
        migrations.AlterField(
            model_name='matchevent',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удален'),
        ),
        migrations.AlterField(
            model_name='matchevent',
            name='oc_group_name',
            field=models.CharField(max_length=255, verbose_name='Название группы Рынка Коэффициентов'),
        ),
        migrations.AlterField(
            model_name='matchevent',
            name='oc_name',
            field=models.CharField(max_length=255, verbose_name='Название исхода'),
        ),
        migrations.AlterField(
            model_name='matchevent',
            name='oc_pointer',
            field=models.CharField(max_length=100, verbose_name='Поинтер для API'),
        ),
        migrations.AlterField(
            model_name='matchevent',
            name='oc_rate',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Коэффициент'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='api_id',
            field=models.IntegerField(verbose_name='Api Id'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удалена'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='name_en',
            field=models.CharField(max_length=255, verbose_name='Название на английском'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='request_type',
            field=models.CharField(default='line', max_length=4, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='api_id',
            field=models.IntegerField(verbose_name='Api Id'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t_country', to='sport_events.country', verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удален'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='name_en',
            field=models.CharField(max_length=255, verbose_name='Название на английском'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='request_type',
            field=models.CharField(default='line', max_length=4, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t_sport', to='sport_events.sport', verbose_name='Спорт'),
        ),
    ]
