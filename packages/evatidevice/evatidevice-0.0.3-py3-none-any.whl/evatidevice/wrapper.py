import time
from functools import wraps


def retry_wrapper(exception_handler=Exception, tries=3, delay=3):
    def _decorator(f):
        @wraps(f)
        def _decorated(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except exception_handler as e:
                    print(f"{e}, Retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= 2
            return f(*args, **kwargs)
        return _decorated
    return _decorator
