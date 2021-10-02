from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Transcript(models.Model):
    podcast_name = models.CharField(max_length=200)
    alias = models.CharField(max_length=50)
    all_text = ""
    color = "green"

    def __str__(self):
        return self.podcast_name


class Podcast(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    audio_bucket_id = models.CharField(max_length=300)
    audio_file_id = models.CharField(max_length=300)
    transcript_bucket_id = models.CharField(max_length=300)
    transcript_file_id = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    episode_number = models.IntegerField()
    author = models.CharField(max_length=20)
    publish_date = models.DateTimeField()
    rss_url = models.CharField(max_length=300)
    duration = models.IntegerField()

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    favorites = ArrayField(models.CharField(max_length=10, blank=True), size=10, default=list)
    password = models.CharField(max_length=100)
    google_login_info = models.CharField(max_length=300)

    def __str__(self):
        return self.username
