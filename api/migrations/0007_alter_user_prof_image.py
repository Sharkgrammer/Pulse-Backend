# Generated by Django 4.0.6 on 2022-08-03 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_user_prof_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='prof_image',
            field=models.ImageField(blank=True, upload_to='profs', verbose_name='Profile Image'),
        ),
    ]