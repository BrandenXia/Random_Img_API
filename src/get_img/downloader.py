import requests
import os

from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.traceback import install
from retry import retry

install()
progress = Progress(TextColumn("[bold blue]{task.fields[filename]}"),
                    BarColumn(bar_width=None),
                    "[progress.percentage]{task.percentage:>3.1f}%",
                    "•",
                    DownloadColumn(),
                    "•",
                    TransferSpeedColumn(),
                    "•",
                    TimeRemainingColumn())

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/91.0.4472.124 Safari/537.36"}


@retry(tries=3, delay=1)
def download(url: str, path: str, filename: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

    try:
        header = requests.head(url, headers=headers)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError("Connection failed")
    try:
        total_size = int(header.headers.get("Content-Length"))
    except TypeError:
        print("Failed to get file size, maybe because of the network")
        return

    response = requests.get(url, headers=headers, stream=True)
    chunk_size = 1024

    with progress:
        task_id = progress.add_task("Download", filename=filename, total=total_size)
        with open(os.path.join(path, filename), "wb") as f:
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                progress.update(task_id, advance=len(data))
