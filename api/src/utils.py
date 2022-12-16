import time
from functools import wraps


def retry_on(exceptions, times, sleep_sec=1):
    """
    decorator which re-try block of code if given exception happen
    eventually wait few seconds before next re-try
    usage:

    @retry_on((AttributeError,), 2, 1)
    def func_will_be_executed_three_times():
        raise AttributeError()
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if not isinstance(e, exceptions):
                        raise  # re-raises unexpected exceptions
                    time.sleep(sleep_sec)
            raise last_exception  # re-raises if attempts are unsuccessful

        return wrapper

    return decorator
