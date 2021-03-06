# Generated by Django 3.1.1 on 2020-09-21 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport_events', '0005_auto_20200921_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='match',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='matchevent',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sport',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
