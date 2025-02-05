import re


def get_file_id_from_url(url: str) -> str:
    match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("No file ID found in the URL")


def get_download_url_from_file_id(file_id: str) -> str:
    return f"https://drive.google.com/u/0/uc?id={file_id}&export=download"
