from django.db import models

# Create your models here.

class Transcript(models.Model):
    podcast_name = models.CharField(max_length=200)
    alias = models.CharField(max_length = 50)
    all_text = "" 

    def __str__(self):
        return self.podcast_name
        