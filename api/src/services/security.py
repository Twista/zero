import bleach


def sanitize(value, is_value=True):
    """
    remove all HTML tags/attributes from given input
    """
    if isinstance(value, dict):
        value = {sanitize(k, False): sanitize(v, True) for k, v in value.items()}
    elif isinstance(value, list):
        value = [sanitize(v, True) for v in value]
    elif isinstance(value, str):
        if is_value:
            value = bleach.clean(value, tags=[], attributes=[], styles=[], strip=True)
    return value
