# Generated by Django 3.2.7 on 2021-09-14 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trascript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('podcast_name', models.CharField(max_length=200)),
                ('alias', models.CharField(max_length=50)),
            ],
        ),
    ]
