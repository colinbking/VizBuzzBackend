# Generated by Django 3.2.7 on 2021-10-03 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_auto_20211002_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='word_info',
            field=models.JSONField(default={'words': []}),
            preserve_default=False,
        ),
    ]