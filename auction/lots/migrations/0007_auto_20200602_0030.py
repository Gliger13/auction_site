# Generated by Django 3.0.6 on 2020-06-01 21:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0006_auto_20200601_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='tags',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lot',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 4, 21, 30, 43, tzinfo=utc)),
        ),
    ]
