from datetime import datetime


def utc_timestamp() -> int:
    """
    return a timestamp in UTC
    """
    return int(datetime.utcnow().timestamp())
