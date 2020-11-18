# Generated by Django 3.0.6 on 2020-11-05 21:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0002_auto_20201105_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='status',
            field=models.CharField(choices=[('W', 'Wining'), ('L', 'Losing')], max_length=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='finish_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 21, 27, 5, 13481, tzinfo=utc)),
        ),
    ]
