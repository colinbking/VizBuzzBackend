from django.test import TestCase
from .models import Transcript


class TestModels(TestCase):
    """
    Class for testing all models.
    """
    def setUp(self) -> None:
        """
        Defines a dummy Transcript object.
        """
        self.transcript = Transcript.objects.create(
            podcast_name='413 Podcast', alias="413")

    def test_transcript_model(self):
        """
        Tests the type and name of the created dummy Transcript object.
        """
        test_one = self.transcript
        self.assertTrue(isinstance(test_one, Transcript))
        self.assertEqual(str(test_one), '413 Podcast')
