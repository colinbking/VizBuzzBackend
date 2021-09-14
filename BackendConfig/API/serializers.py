# Turns models into JSON representation so API user
# can parse the data. Also serializes posted JSON to
# the appropriate model for backend manipulation.

from rest_framework import serializers
from .models import Transcript


class TranscriptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transcript
        fields = ('name', 'alias', 'all_text')
