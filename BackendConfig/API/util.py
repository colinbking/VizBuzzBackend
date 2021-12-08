from .models import User
from rest_framework.exceptions import AuthenticationFailed

import jwt


def validate_token(request, refresh=False):
    if refresh:
        token = request.COOKIES.get('refresh')
    else:
        token = request.COOKIES.get('access')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('JWT token expired')
    user = User.objects.filter(id=payload['id']).first()
    if user:
        print("valid user with id=" + str(user.id))
        return User
    print(user)

    raise AuthenticationFailed('User not Found!')
