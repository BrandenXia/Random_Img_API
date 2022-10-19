import os
from json import loads
from datetime import datetime
from src import dbo
import requests
import argparse
from PIL import Image
import sqlite3
import pydenticon

database = sqlite3.connect("img_info.sqlite3")
cursor = database.cursor()


def get_acg():
    """
    download acg images from api.lolicon.app
    """
    while True:
        try:
            # get context from web
            context = requests.get("https://api.lolicon.app/setu/v2").text
            # get name and pid information
            pid = loads(context)['data'][0]['pid']
            name = loads(context)['data'][0]['title']
            # download image
            rt = os.system("wget https://pixiv.cat/%d.jpg" % (pid,))
            # insert image into database
            if rt == 0:
                img = Image.open("./%d.jpg" % (pid,))
                img_x, img_y = img.size
                dbo.insert(name, "acg", "jpg", "img/%d.jpg" % (pid,), img_x, img_y)
                img.close()
        # stop if interrupted
        except KeyboardInterrupt:
            break


def get_wallpaper():
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
                dbo.insert("wallpaper%d" % (num,), 'wallpaper', 'png', "img/wallpaper%d.png" % (num,), 1920, 1080)
        # stop if interrupted
        except KeyboardInterrupt:
            break


def get_avatar():
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
            dbo.insert("avatar%d" % (num,), 'avatar', 'png', "img/avatar%d.png" % (num,), 240, 240)
            print("avatar%d.png generated" % (num,))
        except KeyboardInterrupt:
            break


# Still need to improve this part
def arg_parse():
    """
    parse arguments from command line
    """
    parser = argparse.ArgumentParser(description='get images from internet')
    parser.add_argument('--acg', action='store_true', help='get good images')
    parser.add_argument('--wallpaper', action='store_true', help='get wallpaper')
    parser.add_argument('--avatar', action='store_true', help='generate avatars')
    args = parser.parse_args()
    return args


def init():
    """
    go to img directory, initialize database, and get arguments from command line
    """
    # go to img directory
    os.chdir("img")
    # initialize database
    dbo.init()
    # get arguments from command line
    args = arg_parse()
    # Will edit this part later
    # Make it more flexible
    if args.acg:
        get_acg()
    if args.avatar:
        get_avatar()
    if args.wallpaper:
        get_wallpaper()


if __name__ == "__main__":
    init()
