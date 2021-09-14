from django.urls import include, path
from rest_framework import routers
from .views import homePageView, TranscriptViewSet, TranscriptView

# Routers ensure requests end up at right source dynamically, 
# they work with viewsets to route requests.
router = routers.DefaultRouter()
router.register(r'transcripts', TranscriptViewSet)

urlpatterns = [
    path('', homePageView, name='home'),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('view-transcripts', TranscriptView.as_view(), name="simpleView")
]


