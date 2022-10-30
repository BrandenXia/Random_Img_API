import requests

from json import loads

from random_img_api.src.config import config

# get config
_config = config.Config("config.json")
r18 = _config.get("r18")


def get_url(type: str) -> list[str, str] or None:
    """
    :param type: the img type(acg / wallpaper)
    :return: [img url, filename], None if invalid type
    """
    if type == "acg":
        return acg()
    elif type == "wallpaper":
        return wallpaper()
    else:
        return


def acg() -> list[str, str]:
    """
    :return: [acg img url, acg filename]
    """
    # get the acg img content
    content = requests.get("https://api.lolicon.app/setu/v2?r18=" + str(r18)).text
    # get name and url information
    name = loads(content)['data'][0]['title']
    url = "https://pixiv.cat/%d.jpg" % loads(content)['data'][0]['pid']
    return [url, name]


def wallpaper() -> list[str, str]:
    """
    :return: [wallpaper img url, wallpaper filename]
    """
    # get wallpaper content
    content = requests.get("https://img.xjh.me/random_img.php?return=json&type=bg&ctype=nature").text
    # get url information
    url = "https:%s" % loads(content)['img']
    name = url.split("/")[-1].split(".")[0]
    return [url, name]
