# Generated by Django 3.0.6 on 2020-05-27 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200527_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='secret_email_token',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='verification_email_sent_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='image',
            field=models.ImageField(default='/users/base_icon.jpg', upload_to='media'),
        ),
    ]
