import requests

from json import loads


def get_url(type: str) -> tuple[str, str] or None:
    """
    :param type: the img type(acg / wallpaper)
    :return: [img url, filename], None if invalid type
    """
    if type == "acg":
        return acg()
    elif type == "wallpaper":
        return wallpaper()
    else:
        raise Exception("Invalid Type: %s" % type)


def acg() -> tuple[str, str]:
    """
    :return: [acg img url, acg filename]
    """
    # get config
    from random_img_api.src.config import config
    _config = config.Config("config.json")
    r18 = _config.get("r18")
    # get the acg img content
    content = requests.get("https://api.lolicon.app/setu/v2?r18=" + str(r18)).text
    # get name and url information
    name = loads(content)['data'][0]['title']
    url = "https://pixiv.cat/%d.jpg" % loads(content)['data'][0]['pid']
    return url, name


def wallpaper() -> tuple[str, str]:
    """
    :return: [wallpaper img url, wallpaper filename]
    """
    # get wallpaper content
    content = requests.get("https://img.xjh.me/random_img.php?return=json&type=bg&ctype=nature").text
    # get url information
    url = "https:%s" % loads(content)['img']
    name = url.split("/")[-1].split(".")[0]
    return url, name


def ai() -> tuple[str, str]:
    """
    :return: [generated img url, generated img id]
    """
