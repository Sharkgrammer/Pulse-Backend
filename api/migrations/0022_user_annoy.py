# Generated by Django 4.0.6 on 2022-11-09 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20221107_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='annoy',
            field=models.BooleanField(default=False, verbose_name='Verified'),
        ),
    ]
