# Generated by Django 4.0.6 on 2022-08-26 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_like_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('count', models.IntegerField(default=0)),
                ('deleted', models.BooleanField(default=False)),
                ('field1', models.CharField(blank=True, default='', max_length=255)),
                ('field2', models.CharField(blank=True, default='', max_length=255)),
                ('field3', models.CharField(blank=True, default='', max_length=255)),
                ('field4', models.CharField(blank=True, default='', max_length=255)),
                ('field5', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Interest_User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('deleted', models.BooleanField(default=False)),
                ('field1', models.CharField(blank=True, default='', max_length=255)),
                ('field2', models.CharField(blank=True, default='', max_length=255)),
                ('field3', models.CharField(blank=True, default='', max_length=255)),
                ('field4', models.CharField(blank=True, default='', max_length=255)),
                ('field5', models.CharField(blank=True, default='', max_length=255)),
                ('interest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.interest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]