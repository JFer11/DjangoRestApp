# Generated by Django 3.1.5 on 2021-02-26 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_articles', '0006_auto_20210222_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]