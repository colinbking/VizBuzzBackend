from rest_framework import viewsets, views
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Transcript
from .serializers import TranscriptSerializer


def homePageView(request):
    return HttpResponse('Hello, World!')


# ModelViewSets are special views that handle GET and POST requests for a specific model.
class TranscriptViewSet(viewsets.ModelViewSet):
    """[View to see a transcript]

    """
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer


# Simple Views, an alternative to ViewSets, require specific declaration for each action.
class TranscriptView(views.APIView):
    # authentication_classes tbd
    # permission_classes tbd

    def get(self, request, format=None):
        """
        Return 3 podcast transcripts.
        """
        # uses internal django parser based on content-type header
        # data = request.data
        dummy_transcript_1 = {"name": "hello1", "alias": "world1", "color": "green", "all_text": "Hello1 Dr. Wallach"}
        dummy_transcript_2 = {"name": "hello2", "alias": "world2", "color": "red", "all_text": "Hello2 Dr. Wallach"}
        dummy_transcript_3 = {"name": "hello3", "alias": "world3", "color": "green", "all_text": "Hello3 Dr. Wallach"}
        dummy_response = {"transcripts": [dummy_transcript_1, dummy_transcript_2, dummy_transcript_3]}
        return Response(dummy_response)