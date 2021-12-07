from django.test import TestCase
from .models import Podcast


class TestModels(TestCase):
    """
    Class for testing all models.
    """
    def setUp(self) -> None:
        """
        Defines a dummy Podcast object.
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

    def test_podcast_model(self):
        """
        Tests the type and name of the created dummy Podcast object.
        """
        test_podcast = self.podcast
        self.assertTrue(isinstance(test_podcast, Podcast))
        self.assertEqual(str(test_podcast), 'TestPodcast')
