from boto3.session import Session
from requests_aws_sign import AWSV4Sign


def get_http_auth(service):
    session = Session()
    credentials = session.get_credentials()

    auth = AWSV4Sign(credentials, session.region_name, service)
    return auth
