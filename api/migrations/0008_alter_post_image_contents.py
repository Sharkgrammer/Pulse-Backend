# Generated by Django 4.0.6 on 2022-08-03 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_user_prof_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_contents',
            field=models.ImageField(blank=True, upload_to='posts'),
        ),
    ]
