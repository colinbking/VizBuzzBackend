from django.urls import include, path
from rest_framework import routers
from rest_framework.serializers import as_serializer_error
from .views import *

# Routers ensure requests end up at right source dynamically,
# they work with viewsets to route requests.

urlpatterns = [
    path(
        'api-auth',
        include('rest_framework.urls', namespace='rest_framework')
        ),
    path('view-transcripts', TranscriptView.as_view(), name="simpleView"),
    path('user', UserView.as_view(), name="userView"),
    path('users', UserViewAll.as_view(), name="all_users"),
    path('podcast', PodcastView.as_view(), name="podcastView"),
    path('podcasts', PodcastViewAll.as_view(), name="all_podcasts"),
    path('', HomePageView.as_view(), name="helloworld"),
    path('login', LoginView.as_view(), name='login'),
    path('refresh', RefreshView.as_view(), name="refresh"),
    path('logout', LogoutView.as_view(), name="logout")
]
