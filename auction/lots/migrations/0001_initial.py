# Generated by Django 3.0.6 on 2020-06-01 17:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=256)),
                ('text_description', models.TextField()),
                ('image', models.ImageField(null=True, upload_to='media')),
                ('base_price', models.IntegerField(default=0)),
                ('current_price', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(default=datetime.datetime(2020, 6, 4, 17, 8, 4, tzinfo=utc))),
                ('is_mail_send', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lots', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', 'base_price'],
            },
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bets', to='lots.Lot')),
                ('set_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
