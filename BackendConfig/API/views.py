# from rest_framework import views
# from django.http import HttpResponse, JsonResponse, HttpResponseServerError
# from rest_framework.response import Response
# from .models import Podcast, User
# from .serializers import PodcastSerializer, UserSerializer
# from .Fetcher import Fetcher
# from .util import validate_token
# from rest_framework.exceptions import AuthenticationFailed

# import json
# import boto3
# import uuid
# import jwt, datetime


# class HomePageView(views.APIView):
#     def get(self, request):
#         return HttpResponse('VizBuzz Backend')

# """
# Primary view for querying transcript json documents from s3.
# """
# class TranscriptView(views.APIView):
#     def __init__(self):
#         views.APIView.__init__(self)
#         self.s3 = boto3.client('s3')

#     def get(self, request, format=None):
#         """
#         Return transcript metadata given podcast info.
#         """
#         try:
#             # try url params first
#             podcast_id = request.GET.get("podcast_id", None)
#             if podcast_id:
#                 queried_podcast_data = PodcastSerializer(Podcast.objects.get(id=podcast_id)).data
#                 transcript_file_id = queried_podcast_data["transcript_file_id"]
#                 transcript_bucket_name = queried_podcast_data["transcript_bucket_id"]
#                 return JsonResponse(
#                     json.loads(self.s3.get_object(Bucket=transcript_bucket_name, Key=transcript_file_id)['Body'].read()),
#                     safe=False,
#                     status=200
#                 )
#         except KeyError:
#             return Response("transcript_bucket_id or transcript_file_id not found in request body", status=400)
#         except Exception as e:
#             return Response("failed to get transcript: " + str(e) + " " + str(type(e)), status=400)



# """
# Primary view for CRUD on User objects
# """
# class UserView(views.APIView):
    
#     def get(self, request, format=None):
        
#         try:
#             validate_token(request)
#         except Exception as e:
#             return HttpResponse('Unauthorized: ' + str(e), status=401)
        
#         try:
#             json_data = json.loads(request.body)
#             req_id = json_data["id"]
#             queried_user = UserSerializer(User.objects.get(id=req_id))
#             return JsonResponse(queried_user.data)

#         except KeyError:
#             return Response("id key not found in request body", status=400)
#         except Exception as e:
#             return Response("failed to get User" + str(e), status=400)

#         return HttpResponseServerError("Server Error")


#     # used during user creation
#     def post(self, request, format=None):
#         new_id = uuid.uuid4()
#         try:
#             d = json.loads(request.body)
#             new_user = User(
#                 id=new_id,
#                 name=d['name'],
#                 username=d['username'],
#                 favorites=d['favorites'],
#                 password=d['password'],
#                 google_login_info=d['google_login_info']
#             )
#             new_user.set_password(new_user.password)
#             new_user.save()
#             return JsonResponse({"saved_user_id": new_id}, status=200)

#         except KeyError as e:
#             return Response("Request Format Incorrect: " + str(e), status=400)
#         except Exception as e:
#             return Response("Exception Occurred in trying to create new User: " + str(e), status=500)

#         return HttpResponseServerError("Server Error")


# """
# Primary view for querying all users
# """
# class UserViewAll(views.APIView):

#     def get(self, request):
#         try:
#             validate_token(request)
#         except Exception as e:
#             return HttpResponse('Unauthorized: ' + str(e), status=401)
        
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many = True)
#         response = Response()
#         response.data = serializer.data
#         return response

# """
# Primary view for CRUD on Podcast objects
# """
# class PodcastView(views.APIView):

#     def get(self, request, format=None):
#         """
#         returns a specific Podcast
#         """
#         try:
#             validate_token(request)
#         except Exception as e:
#             return HttpResponse('Unauthorized ' + str(e), status=401)
        
#         try:
#             json_data = json.loads(request.body)
#             req_id = json_data["id"]
#             queried = PodcastSerializer(Podcast.objects.get(id=req_id))
#             return JsonResponse(queried.data)

#         except KeyError:
#             return Response("id key not found in request body", status=400)
#         except Exception as e:
#             return Response("failed to get Podcast, " + str(e), status=400)

#         return HttpResponseServerError("Server Error")

#     def post(self, request, format=None):
#         """
#         creates a podcast entry
#         """
#         try:
#             validate_token(request)
#         except Exception as e:
#             return HttpResponse('Unauthorized ' + str(e), status=401)
        
#         try:
#             d = json.loads(request.body)
#             Podcast(
#                 id=d['id'],
#                 audio_bucket_id=d['audio_bucket_id'],
#                 audio_file_id=d['audio_file_id'],
#                 transcript_bucket_id=d['transcript_bucket_id'],
#                 transcript_file_id=d['transcript_file_id'],
#                 name=d['name'],
#                 episode_number=d['episode_number'],
#                 author=d['author'],
#                 publish_date=d['publish_date'],
#                 rss_url=d['rss_url'],
#                 duration=d['duration'],
#                 word_info=d['word_info']
#             ).save()
#             return JsonResponse({"saved_podcast_id": d["id"]}, status=200)

#         except KeyError as e:
#             return Response("Request Format Incorrect: " + str(e), status=400)
#         except Exception as e:
#             return Response("Exception Occurred in trying to create new Podcast: " + str(e), status=500)

#         return HttpResponseServerError("Server Error")

# """
# Primary view for querying all Podcasts
# """
# class PodcastViewAll(views.APIView):
#     """[View to see all transcripts]
#     """
#     def get(self, request):
#         try:
#             validate_token(request)
#         except Exception as e:
#             return HttpResponse('Unauthorized: ' + str(e), status=401)
        
#         queryset = Podcast.objects.all()
#         serializer = PodcastSerializer(queryset, many = True)
#         response = Response()
        
#         response.data = serializer.data
#         return response


# """
# Primary view for logging in and obtaining refresh and acess tokens. 
# Stores user id in session.
# """
# class LoginView(views.APIView):
#     def post(self, request):
#         username = request.data['username']
#         password = request.data['password']

#         user = User.objects.filter(username=username).first()

#         if user is None:
#             raise AuthenticationFailed('User not found!')
        
#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password!')

#         access_payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
#             'iat': datetime.datetime.utcnow()
#         }

#         refresh_payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
#             'iat': datetime.datetime.utcnow()
#         }

#         access_token = jwt.encode(access_payload, 'secret', algorithm='HS256')
#         refresh_token = jwt.encode(refresh_payload, 'secret', algorithm='HS256')
#         response = Response()

#         response.set_cookie(key='access', value=access_token, httponly=True)
#         response.set_cookie(key='refresh', value=refresh_token, httponly=True)

#         response.data = {
#             'access': access_token,
#             'refresh': refresh_token
#         }

#         request.session['user_id'] = user.id
        
#         return response

# """
# Primary view for refreshing an access token
# """
# class RefreshView(views.APIView):
#     def post(self, request):
#         try:
#             validate_token(request, refresh=True)
#         except Exception as e:
#             return HttpResponse('Unauthorized: ' + str(e), status=401)

#         print("refresher:", request.session.get('user_id', None))
#         requester_id = request.session.get('user_id', None)
        
#         if requester_id:
#             payload = {
#                         'id': requester_id,
#                         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
#                         'iat': datetime.datetime.utcnow()
#                     }

#             access_token = jwt.encode(payload, 'secret', algorithm='HS256')
            
#             response = Response()
#             response.set_cookie(key='access', value=access_token, httponly=True)
#             response.data = {
#                 'access': access_token,
#             }
#             response.set_cookie(key='access', value=access_token, httponly=True)

#             return response
        
#         return HttpResponse('Unauthorized: User not Found', status=401)


# """
# View to Logout, deletes session and tokens
# """
# class LogoutView(views.APIView):
#     def post(self, request):
#         errors = []
#         try:
#             del request.session['user_id']
#             request.session.flush()
#         except KeyError:
#             errors.append("session was not deleted")
#         finally:
#             response = Response()
#             response.delete_cookie('access')
#             response.delete_cookie('refresh')
#             response.data = {
#                 'message': 'success',
#                 'errors': errors
#             }
#             return response