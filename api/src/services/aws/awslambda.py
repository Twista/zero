import json

import boto3

from src.config import current_config


class LambdaResponse:
    def __init__(self, payload, meta, success):
        self._payload = payload.read()
        self.meta = meta
        self.success = success

    @property
    def status_code(self):
        return self.meta.get("HTTPStatusCode")

    @property
    def status(self):
        return self.payload.get("status", False)

    @property
    def request_id(self):
        return self.meta.get("RequestId")

    @property
    def payload(self):
        return json.loads(self._payload.decode("utf-8"))


def get_client():
    try:
        return get_client.client
    except AttributeError:
        if current_config.IS_OFFLINE:
            client = boto3.client('lambda',
                                  aws_access_key_id='aaa',
                                  aws_secret_access_key='bbb',
                                  endpoint_url='http://localhost:3002')
        else:
            client = boto3.client('lambda')
        get_client.client = client

    return get_client.client


def _exec_function(func_name: str, payload: dict, invocation_type="RequestResponse"):
    client = get_client()
    response = client.invoke(FunctionName=func_name, InvocationType=invocation_type, Payload=json.dumps(payload))
    return response


def exec_sync(func_name: str, payload: dict) -> LambdaResponse:
    response = _exec_function(current_config.LAMBDA_PREFIX + func_name, payload)
    return LambdaResponse(
        success=True if not response.get("FunctionError") else False,
        payload=response.get('Payload'),
        meta=response.get("ResponseMetadata")
    )


def exec_async(func_name: str, payload: dict):
    return _exec_function(current_config.LAMBDA_PREFIX + func_name, payload, invocation_type="Event")
