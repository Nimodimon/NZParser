from functools import wraps

from requests.exceptions import ReadTimeout, ConnectionError

def timeout_ignore(func):
    @wraps(func)
    def inner(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except (ReadTimeout, ConnectionError) as e:
                print(e)
                continue
            else:
                break

    return inner

def clear_text(text: str) -> str:
    return text.replace("\n", "").replace("\r", "").replace("  ", "")