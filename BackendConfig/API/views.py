from rest_framework import viewsets, views
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from rest_framework.response import Response
from .models import Podcast, User
from .serializers import PodcastSerializer, UserSerializer
from .Fetcher import Fetcher
from .Transcriber.transcriber import Transcriber
import json
import boto3
import uuid
import os


def homePageView(request):
    return HttpResponse('Hello, World!')


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
        self.s3Fetcher = Fetcher()
        self.transcriber = Transcriber(self.s3Fetcher)

    # upon successful transcription, called to create podcast object in DB.
    def save_podcast_to_db(self, metadata, transcribed_data_filename):
        new_id = uuid.uuid4()
        podcast_object = Podcast(
            id=new_id,
            audio_bucket_id=metadata["audio_bucket_id"],
            audio_file_id=metadata["audio_file_id"],
            transcript_bucket_id=metadata["transcript_bucket_id"],
            transcript_file_id=transcribed_data_filename,
            name=metadata["name"],
            episode_number=metadata["episode_number"],
            author=metadata["author"],
            publish_date=metadata["publish_date"],
            rss_url=metadata["rss_url"],
            duration=metadata["duration"]
        )

        podcast_object.save()
        return str(new_id)
        

    # triggers transcriber to transcribe a podcast from our s3 bucket
    def transcribe_from_bucket_and_key(self, bucket, audio_key, metadata):
        new_file_name = audio_key + ".json"
        transcription_file = self.transcriber.transcribe_from_s3(bucket, audio_key, new_file_name)
        if transcription_file:
            new_id = self.save_podcast_to_db(metadata, new_file_name)
            return JsonResponse({"saved podcast id": new_id})
        return HttpResponseServerError("Error: Transcription of file with rss url=" + metadata["rss_url"] + " failed")

        
    # triggers transcriber to transcribe a podcast from a streaming url
    def transcribe_from_url(self, metadata):
        transcription_file = self.transcriber.transcribe_from_url(metadata["streaming_url"])
        new_file_name = metadata["name"] + str(metadata["episode_number"]) +  ".json"
        if transcription_file:
            try:
                self.s3Fetcher.upload_file("data.json", os.getenv('TRANSCRIPT_BUCKET_NAME'), new_file_name)
            except Exception as e:
                return HttpResponseServerError("Error: upload of json metadata file for podcast with rss_url=" + metadata["rss_url"] + " failed" + str(e))
            
            new_id = self.save_podcast_to_db(metadata, new_file_name)
            return JsonResponse({"saved podcast id": new_id})

        return HttpResponseServerError("Error: Transcription of file with rss url=" + metadata["rss_url"] + " failed")

    def post(self, request, format=None):

        """
        Transcribes an audio file given either
            1. bucket and key
            2. streaming url
        """
        # uses internal django parser based on content-type header
        # data = request.data

        podcast_metadata = json.loads(request.body)
        
        # if grabbing a wav file from s3
        # if "audio_bucket" in podcast_metadata and "audio_key" in podcast_metadata:
        #     bucket = podcast_metadata["audio_bucket"]
        #     audio_key = podcast_metadata["audio_key"]
        #     try:
        #         return self.transcribe_from_bucket_and_key(bucket, audio_key, podcast_metadata)
        #     except Exception as e:
        #         return HttpResponseServerError(e)
        # if streaming_url is supplied in the metadata, transcribe directly from streaming url
        if "streaming_url" in podcast_metadata:
            return self.transcribe_from_url(podcast_metadata)
        else:
            return HttpResponseServerError("Error: unknown keys")


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
