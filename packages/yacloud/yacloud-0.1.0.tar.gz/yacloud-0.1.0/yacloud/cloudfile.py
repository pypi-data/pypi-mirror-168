import os
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError

aws_access_key_id=os.getenv("YC_API_KEY")
aws_secret_access_key=os.getenv("YC_API_SECRET")
if not aws_access_key_id or not aws_secret_access_key:
    raise ValueError("YC_API_KEY and YC_API_SECRET environment variables not cofigured properly")



class CloudFile:
    def __init__(self, bucket_name:str, key:str):
        self._bucket=bucket_name
        self._key=key
        self._session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self._s3 = self._session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
    @property
    def exists(self):
        try:
            self._s3.head_object(Bucket=self._bucket, Key=self._key)
        except ClientError as e:
            return int(e.response['Error']['Code']) != 404
        return True
    def read(self):
        get_object_response = self._s3.get_object(Bucket=self._bucket,Key=self._key)
        return get_object_response['Body'].read()
    def put(self, data):
        return self._s3.put_object(Bucket=self._bucket, Key=self._key, Body=data, StorageClass='COLD')
    def delete(self):
        forDeletion = [{'Key':self._key}]
        return  self._s3.delete_objects(Bucket=self._bucket, Delete={'Objects': forDeletion})
