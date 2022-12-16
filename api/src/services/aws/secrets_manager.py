import base64
import json
from functools import lru_cache

import boto3
from botocore.exceptions import ClientError

from tmighty.caching import get_ttl_hash
from tmighty.utils import Singleton


class SecretsManager(metaclass=Singleton):
    secret = None
    secrets = {}

    @lru_cache()
    def _get_secret_value(self, secret_name, ttl=get_ttl_hash(seconds=60 * 5)):
        if secret_name in self.secrets:
            return self.secrets[secret_name]

    def get_secret(self, secret_name):
        value = self._get_secret_value(secret_name)
        if value:
            return value
        region_name = 'ca-central-1'

        # Create a Secrets Manager client
        client = boto3.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                self.secrets[secret_name] = json.loads(get_secret_value_response['SecretString'])
                return self.secrets[secret_name]
            else:
                self.secrets[secret_name] = json.loads(base64.b64decode(get_secret_value_response['SecretBinary']))
                return self.secrets[secret_name]
