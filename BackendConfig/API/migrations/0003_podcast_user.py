# Generated by Django 3.2.7 on 2021-09-29 04:00

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_rename_trascript_transcript'),
    ]

    operations = [
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('s3_audio_id', models.CharField(max_length=300)),
                ('s3_transcript_id', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=300)),
                ('episode_number', models.IntegerField()),
                ('author', models.CharField(max_length=20)),
                ('publish_date', models.DateTimeField()),
                ('rss_url', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('favorites', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), size=10)),
                ('password', models.CharField(max_length=100)),
                ('google_login_info', models.CharField(max_length=300)),
            ],
        ),
    ]
