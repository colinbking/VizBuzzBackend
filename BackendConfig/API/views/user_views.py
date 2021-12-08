from rest_framework import views
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from rest_framework.response import Response
from ..models import User
from ..serializers import UserSerializer
from ..util import validate_token

import json
import uuid

"""
Primary view for CRUD on User objects
"""
class UserView(views.APIView):
    
    def get(self, request, format=None):
        
        try:
            validate_token(request)
        except Exception as e:
            return HttpResponse('Unauthorized: ' + str(e), status=401)
        
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


    # used during user creation
    def post(self, request, format=None):
        new_id = uuid.uuid4()
        try:
            d = json.loads(request.body)
            new_user = User(
                id=new_id,
                name=d['name'],
                username=d['username'],
                favorites=d['favorites'],
                password=d['password'],
                google_login_info=d['google_login_info']
            )
            new_user.set_password(new_user.password)
            new_user.save()
            return JsonResponse({"saved_user_id": new_id}, status=200)

        except KeyError as e:
            return Response("Request Format Incorrect: " + str(e), status=400)
        except Exception as e:
            return Response("Exception Occurred in trying to create new User: " + str(e), status=500)

        return HttpResponseServerError("Server Error")


"""
Primary view for querying all users
"""
class UserViewAll(views.APIView):

    def get(self, request):
        try:
            validate_token(request)
        except Exception as e:
            return HttpResponse('Unauthorized: ' + str(e), status=401)
        
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many = True)
        response = Response()
        response.data = serializer.data
        return response
