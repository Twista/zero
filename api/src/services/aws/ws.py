import requests

from src.config import current_config
from src.services.aws import get_http_auth


def _get_auth():
    if current_config.IS_OFFLINE:
        return None

    return get_http_auth("execute-api")


def post_to_connection(conn_id, message):
    url = f"{current_config.WS_API}@connections/{conn_id}"
    resp = requests.post(url, json=message, auth=_get_auth())
    return resp
