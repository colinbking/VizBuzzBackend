from rest_framework import views
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from ..models import Podcast
from ..serializers import PodcastSerializer

import json
import boto3



class HomePageView(views.APIView):
    def get(self, request):
        return HttpResponse('VizBuzz Backend')

"""
Primary view for querying transcript json documents from s3.
"""
class TranscriptView(views.APIView):
    def __init__(self):
        views.APIView.__init__(self)
        self.s3 = boto3.client('s3')

    def get(self, request, format=None):
        """
        Return transcript metadata given podcast info.
        """
        try:
            # try url params first
            podcast_id = request.GET.get("podcast_id", None)
            if podcast_id:
                queried_podcast_data = PodcastSerializer(Podcast.objects.get(id=podcast_id)).data
                transcript_file_id = queried_podcast_data["transcript_file_id"]
                transcript_bucket_name = queried_podcast_data["transcript_bucket_id"]
                return JsonResponse(
                    json.loads(self.s3.get_object(Bucket=transcript_bucket_name, Key=transcript_file_id)['Body'].read()),
                    safe=False,
                    status=200
                )
        except KeyError:
            return Response("transcript_bucket_id or transcript_file_id not found in request body", status=400)
        except Exception as e:
            return Response("failed to get transcript: " + str(e) + " " + str(type(e)), status=400)

