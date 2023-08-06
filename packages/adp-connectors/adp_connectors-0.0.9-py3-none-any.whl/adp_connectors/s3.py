import json
import boto3
from .base import Connector


class S3Connector(Connector):

    def __init__(self, config_from_local=False, mount_path='/cos-credentials', secret_file='s3.secrets'):
        super().__init__(config_from_local, mount_path, secret_file)

    def _get_client_from_oc(self, mount_path):
        with open(f'{mount_path}/aws_access_key_id', 'r') as secret_file:
            aws_access_key_id = secret_file.read()
        with open(f'{mount_path}/aws_secret_access_key', 'r') as secret_file:
            aws_secret_access_key = secret_file.read()
        return boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

    def _get_client_from_local(self, secret_file):
        with open(secret_file, 'r') as f:
            credentials = json.load(f)
        return boto3.client(
            's3',
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key']
        )

    def get_object(self, obj, bucket):
        # obj: filename
        # bucket: bucket is required
        return json.loads(self.client.get_object(Bucket=bucket, Key=obj)['Body'].read().decode('utf-8'))

    def list_objects(self, target):
        """
        List the first 30 objects in the target bucket.
        :param target: name of the bucket
        :return: list of response contents
        """
        response = self.client.list_objects_v2(Bucket=target, MaxKeys=30)
        if 'Contents' in response:
            return response['Contents']
        else:
            return []

    def list_all_objects(self, target):
        """
        List the all object ETags in the target bucket.
        :param target: name of the bucket
        :return: the complete list of all objects
        """
        response = self.client.list_objects(Bucket=target)
        if 'Contents' in response:
            contents = response['Contents']

            while response['IsTruncated']:
                response = self.client.list_objects(Bucket=target, ContinuationToken=response['NextContinuationToken'])
                contents += response['Contents']

            return contents
        else:
            return []

    def copy_object(self, source, to_bucket, target_name):
        """
        Copy a file to another bucket
        :param source: from_bucket/file_name
        :param to_bucket: target bucket name
        :param target_name: new file name after copied
        :return: None
        """
        self.client.copy_object(CopySource=source, Bucket=to_bucket, Key=target_name)

    def delete_object(self, bucket, key):
        """
        Delete an object
        :param bucket: bucket name
        :param key: file name
        :return: None
        """
        self.client.delete_object(Bucket=bucket, Key=key)
