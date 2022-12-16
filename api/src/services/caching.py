import time


def get_ttl_hash(seconds=60) -> int:
    """
    Return the same value withing `seconds` time period
    handy for use with @functools.lru_cache as a parameter for invalidation

    @lru_cache()
    def get_some_value(key, _ttl=get_ttl_hash(seconds=10)):
        ....
    """
    return round(time.time() // seconds)
