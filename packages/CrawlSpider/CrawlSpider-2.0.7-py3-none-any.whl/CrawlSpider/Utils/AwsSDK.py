import os.path

import boto3
from botocore import paginate

ks = {
    # 'service_name',
    # 'region_name',
    'api_version',
    'use_ssl',
    'verify',
    'endpoint_url',
    'aws_access_key_id',
    'aws_secret_access_key',
    'aws_session_token',
    'config',
}

class MyFile:
    content = None
    def write(self, data: bytes):
        self.content = data
    def read(self, n=0):
        if not n:
            return self.content
        else:
            return self.content[:n]
    def close(self):
        self.content = None

class AwsSDK:

    def __init__(self, service_name='s3', region_name='cn-north-1', bucket_name='', **kwargs):
        kws = {k:kwargs.get(k) for k in ks}

        self._service_name = service_name
        self.s3 = boto3.resource(service_name, region_name, **kws)
        self.s3Client = boto3.client(service_name, region_name, **kws)
        self.bucket_name = bucket_name



    @property
    def service_name(self):
        return self._service_name

    def getBuckets(self):

        return [bucket.name for bucket in self.s3.buckets.all()]

    def getBucket(self, bucket_name):
        return self.s3.Bucket(bucket_name or self.bucket_name)

    def uploadFile(self, fileKey, fileName=None, stream=None, bucket_name=None):
        # Upload a new file
        if not any([fileName, stream]):
            raise ValueError(f"fileName, stream 不能同时为空")
        if not stream:
            stream = open(fileName, 'rb')
        if not hasattr(stream, 'read'):
            raise AttributeError(f"stream hasn't read attribute")
        bucket = self.getBucket(bucket_name)
        res = bucket.upload_fileobj(stream, Key=fileKey)

        stream.close()
        return res




    def getDirs(self, bucket_name=None):
        paginator = self.s3Client.get_paginator('list_objects')
        result: paginate.PageIterator = paginator.paginate(Bucket=bucket_name or self.bucket_name, Delimiter='/')
        return [prefix.get('Prefix') for prefix in result.search('CommonPrefixes')]


    def getObjContent(self, fileKey, fileName=None, bucket_name=''):
        file = MyFile()
        content = b''
        bucket = self.getBucket(bucket_name)
        if fileName:
            ret = bucket.download_file(fileKey, fileName)
        else:
            ret = bucket.download_fileobj(fileKey, file)
            content = file.content
        return ret, content







