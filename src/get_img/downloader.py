import requests
import os
import time
import multitasking

from rich.progress import Progress
from rich.traceback import install
from retry import retry

from src import config

install()

download_config = config.Config("download.json")
connection_num = download_config.get("connection_num")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/91.0.4472.124 Safari/537.36"}


def split(file_size: int, connection: int) -> list[tuple[int, int]]:
    step = file_size // connection + 1
    download_range = []
    for i in range(0, connection):
        start = i * step
        end = start + step - 1
        if end > file_size:
            end = file_size
        download_range.append((start, end))
    return download_range


def download(url: str, path: str, filename: str) -> None:
    header = requests.head(url, headers=headers)
    file_size = header.headers.get('Content-Length')

    if file_size is not None:
        file_size = int(file_size)
    else:
        raise Exception("File size is None")

    if not os.path.exists(path):
        os.mkdir(path)

    file = open(os.path.join(path, filename), "wb")

    with Progress() as progress:
        task = progress.add_task("[cyan]Downloading %s" % filename, total=file_size)

        @retry(tries=3, delay=1)
        @multitasking.task
        def download_thread(start: int, end: int) -> None:
            _headers = headers.copy()
            _headers["Range"] = "bytes=%d-%d" % (start, end)

            response = requests.get(url, headers=_headers, stream=True)
            chunk_size = 1024
            chunks = []
            for data in response.iter_content(chunk_size=chunk_size):
                chunks.append(data)
                progress.update(task, advance=chunk_size)
            file.seek(start)
            for chunk in chunks:
                file.write(chunk)

        download_range = split(file_size, connection_num)
        for start, end in download_range:
            download_thread(start, end)
            time.sleep(0.01)
        multitasking.wait_for_tasks()
    file.close()
