import os
import json
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
    while True:
        try:
            context = json.loads(requests.get("https://api.lolicon.app/setu/v2?size=original&size=regular&r18=1").text)
            pid = context['data'][0]['pid']
            name = context['data'][0]['title']
            rt = os.system(f"""wget https://pixiv.cat/{pid}.jpg""")
            if rt == 0:
                img = Image.open(f"""./{pid}.jpg""")
                img_x, img_y = img.size
                dbo.insert(name, "acg", "jpg", f"""img/{pid}.jpg""", img_x, img_y)
        except KeyboardInterrupt:
            break


def get_wallpaper():
    while True:
        num = int(round(datetime.now().timestamp() * 10000))
        try:
            rt = os.system(f"""wget -O wallpaper{num}.png https://unsplash.it/1920/1080?random""")
            if rt == 0:
                dbo.insert(f"""wallpaper{num}""", 'wallpaper', 'png', f"""img/wallpaper{num}.png""", 1920, 1080)
        except KeyboardInterrupt:
            break


def get_avatar():
    while True:
        num = int(round(datetime.now().timestamp() * 10000))
        try:
            generator = pydenticon.Generator(10, 10)
            avatar = generator.generate(str(num), 240, 240)
            avatar_write = open(f"""avatar{num}.png""", "wb")
            avatar_write.write(avatar)
            avatar_write.close()
            dbo.insert(f"""avatar{num}""", 'avatar', 'png', f"""img/avatar{num}.png""", 240, 240)
            print(f"""Created avatar{num}""")
        except KeyboardInterrupt:
            break


# Still need to improve the argues the
def arg_parse():
    parser = argparse.ArgumentParser(description='Get images from internet')
    parser.add_argument('--acg', action='store_true', help='Get good images')
    parser.add_argument('--wallpaper', action='store_true', help='Get wallpaper')
    parser.add_argument('--avatar', action='store_true', help='Generate avatars')
    args = parser.parse_args()
    return args


def init():
    os.chdir("img")
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
