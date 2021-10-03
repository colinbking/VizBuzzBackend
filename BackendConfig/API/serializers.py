# Turns models into JSON representation so API user
# can parse the data. Also serializes posted JSON to
# the appropriate model for backend manipulation.

from rest_framework import serializers
from .models import Transcript, Podcast, User


class TranscriptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transcript
        fields = ('name', 'alias', 'color', 'all_text')


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = (
                'id',
                'audio_bucket_id',
                'audio_file_id',
                'transcript_bucket_id',
                'transcript_file_id',
                'name',
                'episode_number',
                'author',
                'publsih_date',
                'rss_url',
                'duration'
                )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
                'id',
                'name',
                'username',
                'favorites',
                'password',
                'google_login_info'
                )
