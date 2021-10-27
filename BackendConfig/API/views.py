from rest_framework import viewsets, views
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from rest_framework.response import Response
from .models import Podcast, User
from .serializers import PodcastSerializer, UserSerializer
from .Transcriber.transcriber import Transcriber
import json
import boto3

def homePageView(request):
    return HttpResponse('Hello, World!')


class TranscriptView(views.APIView):
    # def __init__(self):
    #     super()

    def get(self, request, format=None):
        """
        Return transcript metadata given podcast info.
        """
        try:
            # try url params first
            transcript_bucket_id = request.GET.get("transcript_bucket_id", None)
            transcript_file_id = request.GET.get("transcript_file_id", None)
            if transcript_bucket_id is not None and transcript_file_id is not None:
                return JsonResponse(json.loads(self.s3.get_object(Bucket=transcript_bucket_id, Key=transcript_file_id)['Body'].read()), safe=False, status=200)

            # else attempt json
            json_data = json.loads(request.body)
            transcript_bucket_id = json_data['transcript_bucket_id']
            transcript_file_id = json_data['transcript_file_id']
            s3 = boto3.client('s3')
            return JsonResponse(json.loads(s3.get_object(Bucket=transcript_bucket_id, Key=transcript_file_id)['Body'].read()), safe=False, status=200)

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
            return HttpResponseServerError(e)
        except Exception as e:
            print("failed to transcribe audio file with key: ", audio_key, e)
            return HttpResponseServerError(e)
        return HttpResponseServerError("unknown error")

        
# Simple Views, an alternative to ViewSets, require specific declaration for each action.
class TestUploadDataView(views.APIView):
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
            name = json_data["name"]
            self.transcriber.upload_metadata(name)
            return JsonResponse({"uploaded_name": name})

        except KeyError as e:
            print(e)
            return HttpResponseServerError(e)
        except Exception as e:
            print("failed to upload audio data", e)
            return HttpResponseServerError(e)
        return HttpResponseServerError("unknown error")

