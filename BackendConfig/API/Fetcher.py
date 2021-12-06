import boto3
import json


class Fetcher:

    def __init__(self):
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')

    def fetchMetadata(self, filename, bucket, key):
        self.s3_resource.Bucket(bucket).download_file(key, "metadata/" + filename)
        try:
            with open("metadata/" + filename) as f:
                data = json.load(f)
                return data
        except (IOError, FileNotFoundError) as e:
            print("No file found, or IO failure on file: ", e)
        except Exception as e:
            print("Unknown Exception found: ", e)

    def upload_file(self, old_name, location, new_name):
        self.s3_client.upload_file(old_name, location, new_name)