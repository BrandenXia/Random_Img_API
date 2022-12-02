import rich_click as click
import os

from rich.console import Console

from random_img_api.src import dbo
from random_img_api.src.config import config

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
        from random_img_api.src.get_img.get_url import get_url
        info = get_url(type)
    except KeyboardInterrupt:
        return 1

    # img name and path
    img_name = info[1]
    img_file_path = os.path.join(img_path, "%s.jpg" % img_name)

    # download img
    from random_img_api.src.get_img import downloader
    rt = downloader.download(info[0], img_path, "%s.jpg" % img_name)
    # if failed, return exit code
    # 1: download failed
    if rt == 1:
        console.print("[bold red]Connection Error")
        return 1
    # 2: failed to get image size
    elif rt == 2:
        console.print("[bold red]Failed to get image size")
        return 2
    # download canceled
    elif rt == 3:
        return 3

    # print download info
    console.print("[cyan]Downloaded image: [bold yellow]%s.jpg[/bold yellow]" % img_name)

    # get image size
    from PIL import Image
    # insert info into database
    img = Image.open(img_file_path)
    img_x, img_y = img.size
    # insert into database
    dbo.insert(info[1], type, "jpg", img_file_path, img_x, img_y)

    return 0


def generator(type: str) -> None:
    # get generated image filename
    if type == "avatar":
        from random_img_api.src.get_img.gen_avatar import gen_avatar
        filename = gen_avatar()
    else:
        return
    # insert into database
    dbo.insert(filename, type, "png", os.path.join(img_path, filename), 200, 200)
    console.print("[cyan]Generated image: [bold yellow]%s.png[/bold yellow]" % filename)


@click.command()
@click.option("--type", "-t", default="acg", type=click.Choice(["acg", "wallpaper", "avatar", "ai"]),
              help="The type of image to download")
@click.option("--num", "-n", default=0, type=int, help="The number of images to download")
def get(type, num):
    """
    Get image from internet or generate by program
    """
    # get file type
    if type == "acg" or type == "wallpaper":
        action = "download"
    elif type == "avatar":
        action = "generate"
    elif type == "ai":
        action = "ai"
    else:
        console.print("[bold red]Unknown type: %s" % type)
        return

    if action == "download":
        # count download file amount
        # if num is 0, download forever
        if num == 0:
            count = 0
            while True:
                rt = download(type)
                # if download success, count + 1
                if rt == 0:
                    count += 1
                # if download canceled, break
                elif rt == 3:
                    console.print("[bold green]Download canceled")
                    break
        # download num times
        else:
            count = num
            for i in range(num):
                rt = download(type)
                # if return error code, count - 1
                if rt != 0:
                    count -= 1
                    # if download canceled, break
                    if rt == 3:
                        console.print("[bold green]Download canceled")
                        break

        # report download result
        if count == 1:
            console.print("[bold green]Successfully downloaded 1 image")
        elif count > 1:
            console.print("[bold green]Successfully downloaded %d images" % count)

    elif action == "generate":
        # count generate file amount
        # if num is 0, generate forever
        if num == 0:
            count = 0
            while True:
                generator(type)
                count += 1
        # generate num times
        else:
            count = num
            for i in range(num):
                generator(type)

        # report generate result
        if count == 1:
            console.print("[bold green]Successfully generated 1 image")
        elif count > 1:
            console.print("[bold green]Successfully generated %d images" % count)

    elif action == "ai":
        from random_img_api.src.get_img import gen_ai
        prompt = click.prompt("Please input a description about the image to generate", type=str)
        if prompt:
            if num == 0:
                data = gen_ai.generate(prompt)
            else:
                data = gen_ai.generate(prompt, num)
        else:
            console.print("[bold red]Invalid Prompt")
            return

        if data is None:
            console.print("[bold red]AuthenticationError: Please set \"OPENAI_API KEY\"")
            return

        urls = data[0]
        name = data[1]

        for i in range(len(urls)):
            from random_img_api.src.get_img import downloader
            img_name = "%s-%d.png" % (name, i)
            rt = downloader.download(urls[i], img_path, img_name)

            if rt == 1:
                console.print("[bold red]Connection Error")
            # 2: failed to get image size
            elif rt == 2:
                console.print("[bold red]Failed to get image size")
            # download canceled
            elif rt == 3:
                console.print("[bold green]Download canceled")
                break

            console.print("[cyan]Downloaded image: [bold yellow]%s.jpg[/bold yellow]" % img_name)

            from PIL import Image
            # insert info into database
            img_file_path = os.path.join(img_path, img_name)
            img = Image.open(img_file_path)
            img_x, img_y = img.size
            # insert into database
            dbo.insert(img_name, type, "jpg", img_file_path, img_x, img_y)
