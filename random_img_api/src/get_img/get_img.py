import rich_click as click
import os

from PIL import Image
from rich.console import Console

from random_img_api.src import dbo
from random_img_api.src.config import config
from random_img_api.src.get_img import get_url, downloader, gen_avatar

# init database
dbo.init()
console = Console()

# get config
_config = config.Config("config.json")
img_path = _config.get("img_path")

# create image path if not exist
if not os.path.exists(img_path):
    os.makedirs(img_path)


def download(type: str) -> int:
    # get image url and filename
    try:
        info = get_url.get_url(type)
    except KeyboardInterrupt:
        return 1

    # img name and path
    img_name = info[1]
    img_file_path = os.path.join(img_path, "%s.jpg" % img_name)

    # download img
    rt = downloader.download(info[0], img_path, "%s.jpg" % img_name)
    # if failed, return exit code
    if rt != 0:
        return rt

    # insert info into database
    img = Image.open(img_file_path)
    img_x, img_y = img.size
    dbo.insert(info[1], type, "jpg", img_file_path, img_x, img_y)

    return 0


def generator(type: str) -> None:
    if type == "avatar":
        filename = gen_avatar.gen_avatar()
    else:
        return
    dbo.insert(filename, type, "png", os.path.join(img_path, filename), 200, 200)


@click.command()
@click.option("--type", "-t", default="acg", type=click.Choice(["acg", "wallpaper", "avatar"]),
              help="The type of image to download")
@click.option("--num", "-n", default=0, type=int, help="The number of images to download")
def get(type, num):
    """
    Get image from internet or generate by program
    """
    #
    if type == "acg" or type == "wallpaper":
        action = "download"
    elif type == "avatar":
        action = "generate"
    else:
        console.print("[bold red]Unknown type: %s" % type)
        return

    if action == "download":
        count = 0
        if num == 0:
            while True:
                rt = download(type)
                count += 1
                if rt == 1:
                    console.print("[bold green]Download canceled")
                    break
        else:
            for i in range(num):
                rt = download(type)
                count += 1
                if rt != 0:
                    console.print("[bold green]Download canceled")
                    break

        if count == 1:
            console.print("[bold green]Successfully downloaded 1 image")
        elif count > 1:
            console.print("[bold green]Successfully downloaded %d images" % count)
    elif action == "generate":
        count = 0
        if num == 0:
            while True:
                generator(type)
                count += 1
        else:
            for i in range(num):
                generator(type)
                count += 1

        if count == 1:
            console.print("[bold green]Successfully generated 1 image")
        elif count > 1:
            console.print("[bold green]Successfully generated %d images" % count)
