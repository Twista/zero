import json

import boto3


class SQS:

    @classmethod
    def send(cls, queue_name, message):
        return boto3.client('sqs').send_message(
            QueueUrl=queue_name,
            MessageBody=json.dumps(message)
        )