# Generated by Django 3.2.9 on 2022-08-15 19:16

import api.functions.functions
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_post_image_contents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(default=api.functions.functions.get_today)),
                ('field1', models.CharField(blank=True, default='', max_length=255)),
                ('field2', models.CharField(blank=True, default='', max_length=255)),
                ('field3', models.CharField(blank=True, default='', max_length=255)),
                ('field4', models.CharField(blank=True, default='', max_length=255)),
                ('field5', models.CharField(blank=True, default='', max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_post', to='api.post')),
            ],
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(default=api.functions.functions.get_today)),
                ('field1', models.CharField(blank=True, default='', max_length=255)),
                ('field2', models.CharField(blank=True, default='', max_length=255)),
                ('field3', models.CharField(blank=True, default='', max_length=255)),
                ('field4', models.CharField(blank=True, default='', max_length=255)),
                ('field5', models.CharField(blank=True, default='', max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_user', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
