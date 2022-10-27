import requests

from json import loads

from src import config

download_config = config.Config("download.json")
r18 = download_config.get("r18")


def get_url(type: str) -> list[str, str, str]:
    if type == "acg":
        return acg()


def acg() -> list[str, str, str]:
    context = requests.get("https://api.lolicon.app/setu/v2?r18=" + str(r18)).text
    # get name and pid information
    pid = loads(context)['data'][0]['pid']
    name = loads(context)['data'][0]['title']
    url = "https://pixiv.cat/%d.jpg" % pid
    return [url, name, pid]
