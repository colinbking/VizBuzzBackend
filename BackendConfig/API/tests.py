from django.test import TestCase
from .models import Podcast, User


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
        test_podcast = self.podcast
        test_user = self.user
        self.assertTrue(isinstance(test_podcast, Podcast))
        self.assertTrue(isinstance(test_user, User))
        self.assertEqual(str(test_podcast), 'TestPodcast')
    
    def test_model_str_methods(self):
        """
        Tests the str methods of the created model instances.
        """
        test_podcast = self.podcast
        test_user = self.user
        self.assertEqual(str(test_podcast), 'TestPodcast')
        self.assertEqual(str(test_user), 'johndoe413')
