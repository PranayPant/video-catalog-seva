import re
import time
from functools import wraps
import traceback


def get_file_id_from_url(url: str) -> str:
    match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("No file ID found in the URL")


def get_download_url_from_file_id(file_id: str) -> str:
    return f"https://drive.google.com/u/0/uc?id={file_id}&export=download"


def profile_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function {func.__name__} executed in {execution_time:.2f} seconds")
        return result

    return wrapper


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb = traceback.format_exc()
            print(f"An error occurred in function {func.__name__}: {e}\n{tb}")
            raise

    return wrapper
