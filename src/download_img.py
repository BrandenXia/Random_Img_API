import os
from json import loads
from datetime import datetime
from src import dbo, config
import requests
from PIL import Image
import pydenticon

# define global variables
download_path = ""
r18 = None


def get_acg() -> None:
    """
    download acg images from api.lolicon.app
    """
    while True:
        try:
            # get context from web
            context = requests.get("https://api.lolicon.app/setu/v2?r18=" + str(r18)).text
            # get name and pid information
            pid = loads(context)['data'][0]['pid']
            name = loads(context)['data'][0]['title']
            # download image
            rt = os.system("wget https://pixiv.cat/%d.jpg" % (pid,))
            # insert image into database
            if rt == 0:
                img = Image.open("./%d.jpg" % (pid,))
                img_x, img_y = img.size
                dbo.insert(name, "acg", "jpg", os.path.join(download_path, "%d.jpg") % (pid,), img_x, img_y)
                img.close()
        # stop if interrupted
        except KeyboardInterrupt:
            break


def get_wallpaper() -> None:
    """
    download wallpaper from unsplash.it
    """
    while True:
        # name images with timestamp
        num = int(round(datetime.now().timestamp() * 10000))
        try:
            # get context from web
            rt = os.system("wget -O wallpaper%d.png https://unsplash.it/1920/1080?random" % (num,))
            # insert image into database
            if rt == 0:
                dbo.insert("wallpaper%d" % (num,), 'wallpaper', 'png', os.path.join(download_path, "wallpaper%d.png") %
                           (num,), 1920, 1080)
        # stop if interrupted
        except KeyboardInterrupt:
            break


def get_avatar() -> None:
    """
    generate avatars with pydenticon
    """
    while True:
        # name images with timestamp
        num = int(round(datetime.now().timestamp() * 10000))
        try:
            # Set up a list of foreground colours (taken from Sigil)
            foreground = ["rgb(45,79,255)",
                          "rgb(254,180,44)",
                          "rgb(226,121,234)",
                          "rgb(30,179,253)",
                          "rgb(232,77,65)",
                          "rgb(49,203,115)",
                          "rgb(141,69,170)"]
            background = "rgb(254,254,254)"
            # Instantiate a generator that will create 10x10 block identity icons using SHA1 digest
            generator = pydenticon.Generator(10, 10, foreground=foreground, background=background)
            padding = (20, 20, 20, 20)
            avatar = generator.generate(str(num), 240, 240, padding=padding, output_format="png")
            avatar_write = open("avatar%d.png" % (num,), "wb")
            avatar_write.write(avatar)
            avatar_write.close()
            # insert image into database
            dbo.insert("avatar%d" % (num,), 'avatar', 'png', os.path.join(download_path, "avatar%d.png") % (num,), 240,
                       240)
            print("avatar%d.png generated" % (num,))
        except KeyboardInterrupt:
            break


def init() -> None:
    """
    go to download directory, initialize database, and get arguments from command line
    """
    global download_path, r18
    # read config file
    download_config = config.Config("download.json")
    download_path = download_config.get("download_path")
    r18 = download_config.get("r18")
    # go to download directory
    os.chdir(download_path)
    # initialize database
    dbo.init()


if __name__ == "__main__":
    init()
