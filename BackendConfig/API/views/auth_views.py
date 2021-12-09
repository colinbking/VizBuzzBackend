from django.http.response import HttpResponseForbidden
from rest_framework import views
from django.http import HttpResponse
from rest_framework.response import Response
from ..models import User
from ..util import validate_token
from rest_framework.exceptions import AuthenticationFailed

from jwt import PyJWT
import datetime


class LoginView(views.APIView):
    """
    Primary view for logging in and obtaining refresh and acess tokens.
    Stores user id in session.
    """
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']

            user = User.objects.filter(username=username).first()

            if user is None:
                raise AuthenticationFailed('User not found!')

            if not user.check_password(password):
                raise AuthenticationFailed('Incorrect password!')

            access_payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                'iat': datetime.datetime.utcnow()
            }

            refresh_payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
                'iat': datetime.datetime.utcnow()
            }

            access_token = PyJWT.encode(access_payload, 'secret', algorithm='HS256')
            refresh_token = PyJWT.encode(refresh_payload, 'secret', algorithm='HS256')
            response = Response()

            response.set_cookie(key='access', value=access_token, httponly=True)
            response.set_cookie(key='refresh', value=refresh_token, httponly=True)

            response.data = {
                'access': access_token,
                'refresh': refresh_token
            }

            request.session['user_id'] = user.id
        
            return response
        except Exception as e:
            return HttpResponse("error:" + str(e))


class RefreshView(views.APIView):
    """
    Primary view for refreshing an access token
    """
    def post(self, request):
        try:
            validate_token(request, refresh=True)
        except Exception as e:
            return HttpResponse('Unauthorized: ' + str(e), status=401)

        print("refresher:", request.session.get('user_id', None))
        requester_id = request.session.get('user_id', None)

        if requester_id:
            payload = {
                        'id': requester_id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
                        'iat': datetime.datetime.utcnow()
                    }

            access_token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = Response()
            response.set_cookie(key='access', value=access_token, httponly=True)
            response.data = {
                'access': access_token,
            }
            response.set_cookie(key='access', value=access_token, httponly=True)

            return response

        return HttpResponse('Unauthorized: User not Found', status=401)


class LogoutView(views.APIView):
    """
    View to Logout, deletes session and tokens
    """
    def post(self, request):
        errors = []
        try:
            del request.session['user_id']
            request.session.flush()
        except KeyError:
            errors.append("session was not deleted")
        finally:
            response = Response()
            response.delete_cookie('access')
            response.delete_cookie('refresh')
            response.data = {
                'message': 'success',
                'errors': errors
            }
            return response
