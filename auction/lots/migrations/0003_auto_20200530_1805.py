# Generated by Django 3.0.6 on 2020-05-30 18:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0002_auto_20200530_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 2, 18, 5, 35, tzinfo=utc)),
        ),
    ]
