import urllib.parse
import boto3
# from google.cloud import speech
# import os
# import io
import environ

env = environ.Env()
environ.Env.read_env()
import os

# PREREQUISITES: Download the sanguine file from our backend drive and place it in the Transcriber directory.
# Rename that file to key-file.json.
# Run export GOOGLE_APPLICATION_CREDENTIALS="/<replace-with-the-path-where-the-key-is>/key-file.json"
# Run pip install --upgrade google-cloud-speech


class Transcriber():
    # given a s3 bucket and a key to a specific file, transcribes it and drops it to a
    # our transcript s3 bucket.

    def __init__(self):
        print("connecting to s3 using boto3")
        self.s3 = boto3.client('s3')

    def transcribe(self, bucket, key):
        print("transcribing audio file with key: ", key)
        return self.download_file(bucket, key)
    
    def download_file(self, bucket, key):
        print("downloading file")
        response = self.s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        return True
    
    def upload_metadata(self, filename):
        return os.getcwd()
        #self.s3.upload_file('testfile.txt', env("TRANSCRIPT_BUCKET_NAME"),'/' + filename + '.txt')
        

# # Creates google client
# client = speech.SpeechClient()

# # Full path of the audio file, Replace with your file name
# file_name = os.path.join(os.path.dirname(__file__), "Welcome.wav")

# # Loads the audio file into memory
# with io.open(file_name, "rb") as audio_file:
#     content = audio_file.read()
#     audio = speech.RecognitionAudio(content=content)

# config = speech.RecognitionConfig(
#     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#     audio_channel_count=1,
#     language_code="en-US",
# )

# # Sends the request to google to transcribe the audio
# response = client.recognize(request={"config": config, "audio": audio})

# # Reads the response
# for result in response.results:
#     print("Transcript: {}".format(result.alternatives[0].transcript))
