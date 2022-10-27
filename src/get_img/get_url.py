import requests

from json import loads

from src import config

download_config = config.Config("download.json")
r18 = download_config.get("r18")


def get_url(type: str) -> list[str, str]:
    """
    :param type: the img type(acg / wallpaper)
    :return: [img url, filename]
    """
    if type == "acg":
        return acg()


def acg() -> list[str, str]:
    """
    :return: [acg img url, acg filename]
    """
    # get the acg img content
    context = requests.get("https://api.lolicon.app/setu/v2?r18=" + str(r18)).text
    # get name and url information
    name = loads(context)['data'][0]['title']
    url = "https://pixiv.cat/%d.jpg" % loads(context)['data'][0]['pid']
    return [url, name]


def wallpaper() -> list[str, str]:
    pass
