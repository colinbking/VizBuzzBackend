from rest_framework import viewsets, views
from django.http import JsonResponse, HttpResponseServerError
from rest_framework.response import Response
from .models import Podcast, User
from .serializers import PodcastSerializer, UserSerializer
import json
import boto3


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
                    json.loads(
                        self.s3.get_object(Bucket=transcript_bucket_name, Key=transcript_file_id)['Body'].read()
                    ),
                    safe=False,
                    status=200
                )
        except KeyError:
            return Response("transcript_bucket_id or transcript_file_id not found in request body", status=400)
        except Exception as e:
            return Response("failed to get transcript: " + str(e) + " " + str(type(e)), status=400)


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
            queried_user = UserSerializer(User.objects.get(id=req_id))
            return JsonResponse(queried_user.data)

        except KeyError:
            return Response("id key not found in request body", status=400)
        except Exception as e:
            return Response("failed to get User" + str(e), status=400)

        return HttpResponseServerError("Server Error")

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
            return Response("Request Format Incorrect: " + str(e), status=400)
        except Exception as e:
            return Response("Exception Occurred in trying to create new User: " + str(e), status=500)

        return HttpResponseServerError("Server Error")


class LoginView(views.APIView):

    def get(self, request, format=None):
        """
        returns id of specific user
        """
        try:
            json_data = json.loads(request.body)
            username = json_data["username"]
            queried_user = UserSerializer(User.objects.get(username=username))
            return JsonResponse(queried_user.data)

        except KeyError:
            return Response("id key not found in request body", status=400)
        except Exception as e:
            return Response("failed to get User: " + str(e), status=400)

        return HttpResponseServerError("Server Error")


class PodcastView(views.APIView):

    def get(self, request, format=None):
        """
        returns a specific Podcast
        """
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
