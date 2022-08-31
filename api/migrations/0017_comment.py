# Generated by Django 4.0.6 on 2022-08-24 22:42

import api.functions.functions
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_like_is_post_alter_like_post_alter_post_pid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(default='')),
                ('likes', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(default=api.functions.functions.get_today)),
                ('last_update', models.DateTimeField(default=api.functions.functions.get_today)),
                ('deleted', models.BooleanField(default=False)),
                ('field1', models.CharField(blank=True, default='', max_length=255)),
                ('field2', models.CharField(blank=True, default='', max_length=255)),
                ('field3', models.CharField(blank=True, default='', max_length=255)),
                ('field4', models.CharField(blank=True, default='', max_length=255)),
                ('field5', models.CharField(blank=True, default='', max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented_post', to='api.post')),
            ],
        ),
    ]