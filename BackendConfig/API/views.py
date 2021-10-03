from rest_framework import viewsets, views
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from rest_framework.response import Response
from .models import Podcast, User
from .serializers import PodcastSerializer, UserSerializer
from .Transcriber.transcriber import Transcriber
import json


def homePageView(request):
    return HttpResponse('Hello, World!')


class TranscriptView(views.APIView):
    # authentication_classes tbd
    # permission_classes tbd

    def get(self, request, format=None):
        """
        Return 3 podcast transcripts.
        """
        # uses internal django parser based on content-type header
        # data = request.data
        dummy_transcript_1 = {
            "name": "hello1", "alias": "world1",
            "color": "green", "all_text": "Hello1 Dr. Wallach"}
        dummy_transcript_2 = {
            "name": "hello2", "alias": "world2",
            "color": "red", "all_text": "Hello2 Dr. Wallach"}
        dummy_transcript_3 = {
            "name": "hello3", "alias": "world3",
            "color": "green", "all_text": "Hello3 Dr. Wallach"}
        dummy_response = {
            "transcripts":
            [dummy_transcript_1, dummy_transcript_2, dummy_transcript_3]}
        return Response(dummy_response)


class UserViewSet(viewsets.ModelViewSet):
    """[View to see all Users]
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PodcastViewSet(viewsets.ModelViewSet):
    """[View to see all transcripts]
    """
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer


class UserView(views.APIView):

    def get(self, request, format=None):
        """
        returns a specific user
        """
        try:
            json_data = json.loads(request.body)
            req_id = json_data["id"]

            data = UserSerializer.serialize('json', User.objects.get(id=req_id))
            return JsonResponse(data)

        except KeyError as e:
            return Response("id key not found in request body", status=400)
        except Exception as e:
            return Response("failed to get User" + str(e), status=400)

        return HttpResponseServerError("Server Errpr")

    def post(self, request, format=None):
        """
        creates a user
        """
        try:
            d = json.loads(request.body)
            User(
                id=d['id'],
                name=d['name'],
                username=d['username'],
                favorites=d['favorites'],
                password=d['password'],
                google_login_info=d['google_login_info']
            ).save()
            return JsonResponse({"saved_user_id": d["id"]}, status=200)

        except KeyError as e:
            print(e)
            return Response("Request Format Incorrect", status=400)
        except Exception as e:
            return Response("Exception Occurred in trying to create new User: " + str(e), status=500)

        return HttpResponseServerError("Server Error")


class PodcastView(views.APIView):

    def get(self, request, format=None):
        """
        returns a specific Podcast
        """
        try:
            json_data = json.loads(request.body)
            req_id = json_data["id"]

            data = UserSerializer.serialize('json', User.objects.get(id=req_id))
            return JsonResponse(data)

        except KeyError as e:
            print(e)
        except Exception:
            print("failed to get User with id: ", req_id)

        return HttpResponseServerError()

    def post(self, request, format=None):
        """
        creates a podcast entry
        """
        try:
            d = json.loads(request.body)
            Podcast(
                id=d['id'],
                audio_bucket_id=d['audio_bucket_id'],
                audio_file_id=d['audio_file_id'],
                transcript_bucket_id=d['transcript_bucket_id'],
                transcript_file_id=d['transcript_file_id'],
                name=d['podcast_name'],
                episode_number=d['episode_number'],
                author=d['author'],
                publish_date=d['publish_date'],
                rss_url=d['rss_url']
            ).save()
            return JsonResponse({"saved_podcast_id": d["id"]}, status=200)

        except KeyError as e:
            print(e)
        except Exception:
            print("failed to save User")


# Simple Views, an alternative to ViewSets, require specific declaration for each action.
class AudioUploadView(views.APIView):
    # authentication_classes tbd
    # permission_classes tbd

    def __init__(self):
        self.transcriber = Transcriber()

    def post(self, request, format=None):
        """
        Accepts bucket and key identifier for an audio file and transcribes it
        """
        # uses internal django parser based on content-type header
        # data = request.data

        json_data = json.loads(request.body)

        try:
            bucket = json_data["audio_bucket"]
            audio_key = json_data["audio_key"]
            if self.transcriber.transcribe(bucket, audio_key):
                return JsonResponse({'bucket': bucket, 'audio_key': audio_key})

        except KeyError as e:
            print(e)
        except Exception as e:
            print("failed to transcribe audio file with key: ", audio_key, e)
        return HttpResponseServerError()
