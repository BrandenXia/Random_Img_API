import requests
import os

from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.traceback import install
from retry import retry

# install rich traceback
install()
# config rich progress bar
progress = Progress(TextColumn("[bold blue]{task.fields[filename]}"),
                    BarColumn(bar_width=None),
                    "[progress.percentage]{task.percentage:>3.1f}%",
                    "•",
                    TransferSpeedColumn(),
                    "•",
                    TimeRemainingColumn())

# config headers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/91.0.4472.124 Safari/537.36"}


# retry decorator
@retry(tries=3, delay=1)
def download(url: str, path: str, filename: str) -> None:
    """
    :param url: download url
    :param path: download path
    :param filename: downloaded filename
    :return: None
    """
    # if download path not exists, create it
    if not os.path.exists(path):
        os.makedirs(path)

    # test if url works and get file size
    try:
        response = requests.get(url, headers=headers, stream=True)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError("Connection failed")

    # get file size
    total_size = response.headers.get('Content-Length')
    if total_size is not None:
        total_size = int(total_size)
    else:
        raise TypeError("File size is None")

    # set chunk size
    chunk_size = 1024

    with progress:
        # create progress bar
        task_id = progress.add_task("Download", filename=filename, total=total_size)
        with open(os.path.join(path, filename), "wb") as f:
            for data in response.iter_content(chunk_size=chunk_size):
                # open file and write data
                f.write(data)
                # update progress bar
                progress.update(task_id, advance=len(data))
