from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Podcast(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    audio_bucket_id = models.CharField(max_length=300)
    audio_file_id = models.CharField(max_length=300)
    transcript_bucket_id = models.CharField(max_length=300)
    transcript_file_id = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    episode_number = models.IntegerField()
    author = models.CharField(max_length=200)
    publish_date = models.DateTimeField()
    rss_url = models.CharField(max_length=300)
    duration = models.IntegerField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    favorites = ArrayField(models.CharField(max_length=10, blank=True), size=10, default=list)
    password = models.CharField(max_length=100)
    google_login_info = models.CharField(max_length=300)

    def __str__(self):
        return self.username
