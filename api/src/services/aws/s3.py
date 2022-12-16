from typing import ByteString, IO, Text, Union

import boto3
from botocore.config import Config
from botocore.endpoint import MAX_POOL_CONNECTIONS
from botocore.exceptions import ClientError
from botocore.response import StreamingBody

from src.utils import retry_on


class S3Exception(Exception):
    pass


class NoSuchKey(S3Exception):
    pass


class S3:
    """
    new implementation of S3 with transfer acceleration support
    """

    def __init__(self, bucket, use_accelerate_endpoint=False, max_pool_connections=None):
        self.bucket = bucket
        self._init_boto_s3(use_accelerate_endpoint, max_pool_connections)

    # retry because of boto3 multi-threading error:
    # https://github.com/boto/boto3/issues/801
    @retry_on(KeyError, times=2)
    def _init_boto_s3(self, use_accelerate_endpoint, max_pool_connections):
        s3_config = Config(
            max_pool_connections=max_pool_connections or MAX_POOL_CONNECTIONS,
            s3={'use_accelerate_endpoint': use_accelerate_endpoint}
        )
        self.s3 = boto3.resource(
            service_name='s3',
            config=s3_config
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def put(self, name: str, body: Union[Text, ByteString, IO], public=False, content_type=None) -> dict:
        acl = 'public-read' if public else 'private'
        kwargs = {}
        if content_type:
            kwargs['ContentType'] = content_type

        return self.s3.Object(self.bucket, name).put(Body=body, ACL=acl, **kwargs)

    def get(self, name: str) -> StreamingBody:
        try:
            return self.s3.Object(self.bucket, name).get()["Body"]
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise NoSuchKey("Key '{}' not found".format(name))
            raise S3Exception(e.response[u'Error'][u'Message'])

    def delete(self, name: str) -> dict:
        return self.s3.Object(self.bucket, name).delete()

    def link(self, name: str, http=False) -> str:
        """
        even though there is and option for HttpMethod in generate_presigned_url signature, it has actually not impact
        """
        url = self.s3.meta.client.generate_presigned_url('get_object', ExpiresIn=0,
                                                         Params={'Bucket': self.bucket, 'Key': name})
        if http:
            url = url.replace("https://", "http://")
        return url.split('?', 1)[0]  # the part after `?` needs to be removed
