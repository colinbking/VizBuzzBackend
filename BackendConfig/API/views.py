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
        Return a single podcast transcript.
        """
        # uses internal django parser based on content-type header
        # data = request.data
        temp_dummy_transcript = {"name": "hello", "alias": "world", "color" : "green", "all_text": "Hello Dr. Wallach"}
        return Response(temp_dummy_transcript)
