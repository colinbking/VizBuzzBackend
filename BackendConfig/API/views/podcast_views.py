from rest_framework import views
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from rest_framework.response import Response
from ..models import Podcast
from ..serializers import PodcastSerializer
from ..util import validate_token

import json

"""
Primary view for CRUD on Podcast objects
"""
class PodcastView(views.APIView):

    def get(self, request, format=None):
        """
        returns a specific Podcast
        """
        try:
            validate_token(request)
        except Exception as e:
            return HttpResponse('Unauthorized ' + str(e), status=401)
        
        try:
            json_data = json.loads(request.body)
            req_id = json_data["id"]
            queried = PodcastSerializer(Podcast.objects.get(id=req_id))
            return JsonResponse(queried.data)

        except KeyError:
            return Response("id key not found in request body", status=400)
        except Exception as e:
            return Response("failed to get Podcast, " + str(e), status=400)

        return HttpResponseServerError("Server Error")

    def post(self, request, format=None):
        """
        creates a podcast entry
        """
        try:
            validate_token(request)
        except Exception as e:
            return HttpResponse('Unauthorized ' + str(e), status=401)
        
        try:
            d = json.loads(request.body)
            Podcast(
                id=d['id'],
                audio_bucket_id=d['audio_bucket_id'],
                audio_file_id=d['audio_file_id'],
                transcript_bucket_id=d['transcript_bucket_id'],
                transcript_file_id=d['transcript_file_id'],
                name=d['name'],
                episode_number=d['episode_number'],
                author=d['author'],
                publish_date=d['publish_date'],
                rss_url=d['rss_url'],
                duration=d['duration'],
                word_info=d['word_info']
            ).save()
            return JsonResponse({"saved_podcast_id": d["id"]}, status=200)

        except KeyError as e:
            return Response("Request Format Incorrect: " + str(e), status=400)
        except Exception as e:
            return Response("Exception Occurred in trying to create new Podcast: " + str(e), status=500)

        return HttpResponseServerError("Server Error")

"""
Primary view for querying all Podcasts
"""
class PodcastViewAll(views.APIView):
    """[View to see all transcripts]
    """
    def get(self, request):
        try:
            validate_token(request)
        except Exception as e:
            return HttpResponse('Unauthorized: ' + str(e), status=401)
        
        queryset = Podcast.objects.all()
        serializer = PodcastSerializer(queryset, many = True)
        response = Response()
        
        response.data = serializer.data
        return response

