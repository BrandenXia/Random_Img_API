import os
import requests
import sqlite3
import sys
import json
import pydenticon
from PIL import Image
from datetime import datetime


database = sqlite3.connect("img_info.sqlite3")
cursor = database.cursor()

def get_acg():
    while True:
        try:
            context = requests.get("https://api.lolicon.app/setu/v2?size=original&size=regular&r18=1").text
            pid = json.loads(context)['data'][0]['pid']
            name = json.loads(context)['data'][0]['title']
            rt = os.system(f"""wget https://pixiv.cat/{pid}.jpg""")
            if rt == 0:
                img = Image.open(f"""./{pid}.jpg""")
                img_x, img_y = img.size
                cursor.execute("""INSERT INTO img VALUES (?, ?, ?, ?, ?, ?)""",
                               (name, 'acg', 'jpg', f"""img/{pid}.jpg""", img_x, img_y))
                database.commit()
        except KeyboardInterrupt:
            break


def get_wallpaper():
    while True:
        num = int(round(datetime.now().timestamp() * 10000))
        try:
            rt = os.system(f"""wget -O wallpaper{num}.png https://unsplash.it/1920/1080?random""")
            if rt == 0:
                img = Image.open(f"""./wallpaper{num}.png""")
                img_x, img_y = img.size
                cursor.execute("""INSERT INTO img VALUES (?, ?, ?, ?, ?, ?)""",
                               ("""wallpaper{num}""", 'wallpaper', 'png', f"""img/wallpaper{num}.png""", img_x, img_y))
                database.commit()
        except KeyboardInterrupt:
            break


def get_avatar():
    while True:
        num = int(round(datetime.now().timestamp() * 10000))
        try:
            generator = pydenticon.Generator(10, 10)
            avatar = generator.generate(str(num), 240, 240)
            avatarwrite = open(f"""avatar{num}.png""", "wb")
            avatarwrite.write(avatar)
            avatarwrite.close()
            cursor.execute("""INSERT INTO img VALUES (?, ?, ?, ?, ?, ?)""",
                          (f"""avatar{num}""", 'avatar', 'png', f"""img/avatar{num}.png""", 240, 240))
            database.commit()
        except KeyboardInterrupt:
            break


def init():
    os.chdir("img")
    if len(sys.argv) != 2:
        print("""No options selected
"get_img.py --help" for help""")
        exit()
    else:
        if sys.argv[1] == "--help":
            print("""Usage: get_img.py <options>
Options: 
	--acg       : Get good images
	--avatar    : Generate avatars
	--help      : Show this message
	--wallpaper : Get wallpaper""")
        elif sys.argv[1] == "--acg":
            get_acg()
        elif sys.argv[1] == "--avatar":
            get_avatar()
        elif sys.argv[1] == "--wallpaper":
            get_wallpaper()
        else:
            print("""Invalid argument
"get_img.py --help" for help""")
        
        

if __name__ == "__main__":
    init()
