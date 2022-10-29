import click
import os

from PIL import Image

from src import dbo, config
from src.get_img import downloader, get_url

# init database
dbo.init()

# get config
download_config = config.Config("download.json")
download_path = download_config.get("download_path")


def download(type: str) -> int:
    # get image url and filename
    try:
        info = get_url.get_url(type)
    except KeyboardInterrupt:
        return 1

    # img name and path
    img_name = info[1]
    img_path = os.path.join(download_path, "%s.jpg" % img_name)

    # download img
    rt = downloader.download(info[0], download_path, "%s.jpg" % img_name)
    # if failed, return exit code
    if rt != 0:
        return rt

    # insert info into database
    img = Image.open(img_path)
    img_x, img_y = img.size
    dbo.insert(info[1], type, "jpg", img_path, img_x, img_y)

    return 0


@click.command()
@click.option("--type", "-t", default="acg", type=str, help="the type of image to download")
@click.option("--num", "-n", default=0, type=int, help="the number of images to download")
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
        click.echo("Unknown type: %s" % type)
        return

    if action == "download":
        if num == 0:
            while True:
                rt = download(type)
                if rt == 1:
                    click.echo("Download canceled")
                    break
        else:
            for i in range(num):
                rt = download(type)
                if rt != 0:
                    click.echo("Download canceled")
                    break
    elif action == "generate":
        pass
