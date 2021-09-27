# Turns models into JSON representation so API user
# can parse the data. Also serializes posted JSON to
# the appropriate model for backend manipulation.

from rest_framework import serializers
from .models import *


class TranscriptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transcript
        fields = ('name', 'alias', 'color', 'all_text')


class PodcastSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Podcast
        fields = ('id', 's3_audio_id', 's3_transcript_id', 'name', 'episode_number', 'author', 'publsih_date', 'rss_url')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'favorites', 'password', 'google_login_info')


