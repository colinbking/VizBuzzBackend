from django.test import TestCase
from .models import Podcast, User
from .views import TranscriptView, UserViewSet, PodcastViewSet, UserView, \
                   LoginView, PodcastView


class TestModels(TestCase):
    """
    Class for testing all models.
    """
    def setUp(self) -> None:
        """
        Defines dummy models.
        """
        self.podcast = Podcast.objects.create(
            id='0123456789',
            audio_bucket_id="test",
            audio_file_id="test",
            transcript_bucket_id="vizbuzz-podcast-metadata",
            transcript_file_id="test.wav",
            name="TestPodcast",
            episode_number=1,
            author="TestAuthor",
            publish_date="2021-09-14T00:00:00Z",
            rss_url="www.podcast.com",
            duration=0
        )

        self.user = User.objects.create(
            id="abc",
            name="John Doe",
            username="johndoe413",
            favorites=["TestPodcast1", "TestPodcast2"],
            password="password",
            google_login_info="johndoe@gmail.com"
        )

    def test_model_types(self):
        """
        Tests the types of the created model instances.
        """
        self.assertTrue(isinstance(self.podcast, Podcast))
        self.assertTrue(isinstance(self.user, User))

    def test_model_str_methods(self):
        """
        Tests the str methods of the created model instances.
        """
        self.assertEqual(str(self.podcast), 'TestPodcast')
        self.assertEqual(str(self.user), 'johndoe413')


class TestViews(TestCase):
    """
    Class for testing all views.
    """
    def setUp(self) -> None:
        """
        Defines dummy views.
        """
        self.transcript_view = TranscriptView()
        self.user_view_set = UserViewSet()
        self.podcast_view_set = PodcastViewSet()
        self.user_view = UserView()
        self.login_view = LoginView()
        self.podcast_view = PodcastView()

    def test_view_types(self):
        """
        Tests the types of the created view instances.
        """
        self.assertTrue(isinstance(self.transcript_view, TranscriptView))
        self.assertTrue(isinstance(self.user_view_set, UserViewSet))
        self.assertTrue(isinstance(self.podcast_view_set, PodcastViewSet))
        self.assertTrue(isinstance(self.user_view, UserView))
        self.assertTrue(isinstance(self.login_view, LoginView))
        self.assertTrue(isinstance(self.podcast_view, PodcastView))
