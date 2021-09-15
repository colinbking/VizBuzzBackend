from django.test import TestCase
from .models import Transcript
from .nlp import what_color_is_this_sentence


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

    def test_nlp_very_simple(self):
        """
        Tests if a happy sentence returns "green"
        """
        text = "I had a really amazing day. It was the best day ever!"
        res = what_color_is_this_sentence(text)
        self.assertEqual("green", res)
