import boto3
from django.conf import settings
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)


class Bucket:

    def __init__(self):
        session = boto3.session.Session()
        self.connection = session.client(
            service_name = settings.AWS_SERVICE_NAME,
            aws_access_key_id = settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_S3_SECRET_ACCESS_KEY,
            endpoint_url = settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        result = self.connection.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        else:
            return None
        
    def delete_object(self, key):
        self.connection.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True
    
    
        

bucket = Bucket()
