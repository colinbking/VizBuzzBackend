from django.urls import include, path
from rest_framework import routers
from .views import TranscriptView, AudioUploadView, UserView, PodcastView, \
 UserViewSet, PodcastViewSet, TestUploadDataView

# Routers ensure requests end up at right source dynamically,
# they work with viewsets to route requests.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'podcasts', PodcastViewSet)

urlpatterns = [
    path(
        'api-auth',
        include('rest_framework.urls', namespace='rest_framework')
        ),
    path('view-transcripts', TranscriptView.as_view(), name="simpleView"),
    path('transcribe', AudioUploadView.as_view(), name="transcribeView"),
    path('user', UserView.as_view(), name="userView"),
    path('podcast', PodcastView.as_view(), name="podcastView"),
    path('', include(router.urls)),
    path('test-upload', TestUploadDataView.as_view(), name='testUploadView')
]
