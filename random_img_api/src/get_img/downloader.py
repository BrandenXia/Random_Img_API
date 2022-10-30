import requests
import os

from rich.progress import Progress, TextColumn, BarColumn, TransferSpeedColumn, TimeRemainingColumn

# config rich progress bar
progress = Progress(TextColumn("[bold blue]{task.fields[filename]}"),
                    BarColumn(bar_width=None),
                    "[progress.percentage]{task.percentage:>3.1f}%",
                    "•",
                    TransferSpeedColumn(),
                    "•",
                    TimeRemainingColumn(),
                    transient=True)
# config headers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/91.0.4472.124 Safari/537.36"}


# retry decorator
def download(url: str, path: str, filename: str) -> int:
    """
    :param url: download url
    :param path: download path
    :param filename: downloaded filename
    :return: 0 if download success, 1 if connection error, 2 if failed to get file size, 3 if canceled
    """
    # if download path not exists, create it
    if not os.path.exists(path):
        os.makedirs(path)

    # test if url works and get file size
    try:
        response = requests.get(url, headers=headers, stream=True)
    except requests.exceptions.ConnectionError:
        print("Connection error")
        return 1
    except KeyboardInterrupt:
        return 3

    try:
        # get file size
        total_size = response.headers.get('Content-Length')
        total_size = int(total_size)
    except TypeError:
        print("Failed to get file size")
        return 2
    except KeyboardInterrupt:
        return 3

    # set chunk size
    chunk_size = 1024

    with progress:
        try:
            # create progress bar
            task_id = progress.add_task("Download", filename=filename, total=total_size)
            with open(os.path.join(path, filename), "wb") as f:
                for data in response.iter_content(chunk_size=chunk_size):
                    # open file and write data
                    f.write(data)
                    # update progress bar
                    progress.update(task_id, advance=len(data))
        except KeyboardInterrupt:
            # remove progress bar
            progress.remove_task(task_id)
            progress.stop()
            # remove downloaded file
            os.remove(os.path.join(path, filename))
            return 3
        return 0
