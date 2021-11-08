import boto3
import json

class Fetcher:

    def __init__(self):
        self.s3 = boto3.client('s3')

    def fetchMetadata(self, filename, bucket, key):
        self.s3 = boto3.client('s3')
        s3.Bucket("vizbuzz-podcast-audio-files").download_file(key, "metadata/" + filename)
        try: 
            with open("metadata/" + filename) as f:
                data = json.load(f)
                f.close()
                return data
        except (IOError, FileNotFoundError) as e:
            print("No file found, or IO failure on file: ", e)
        except Exception as e:
            print("Unknown Exception found: ", e)  



