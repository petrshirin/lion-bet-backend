# Generated by Django 3.1.1 on 2020-09-15 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sport_events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='api_id',
        ),
    ]
