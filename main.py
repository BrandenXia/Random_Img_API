from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from typing import Union
from re import match
from random import choice
import os
from src import dbo

# init app
app = FastAPI()
# init database
dbo.init()
# create cursor
if not os.path.exists("img"):
    os.mkdir("img")


# app routes
@app.get("/")
async def main(type_filter: Union[str, None] = Query(default=None, max_length=10, regex=r"^(acg|wallpaper|avatar)$"),
               size: Union[str, None] = Query(default=None, max_length=10, regex=r"^([1-9]\d*|\?)x([1-9]\d*|\?)$")):
    """
    available parameters:
    type_filter: filter by type, default is none, accepts string, available options are "acg", "wallpaper", "avatar"
    size: filter by size, default is none, accepts context string, format is [Number | ?]x[Number | ?], e.g. 1920x1080
    """
    # SELECT PATH, FORMAT FROM img [WHERE] [type = ""] [AND_1] [img_x = ""] [AND_2] [img_y = ""]
    print("type_filter: %s" % type_filter, "size: %s" % size)
    img_x = None
    img_y = None
    if size is not None:
        match_size = match(r"([1-9]\d*|\?)x([1-9]\d*|\?)", size)
        img_x = match_size.group(1)
        img_y = match_size.group(2)
    res = dbo.search(type=type_filter, img_x=img_x, img_y=img_y, needed="PATH,FORMAT")
    try:
        img = choice(res)
    except IndexError:
        return {"error": "no image found"}
    file = open(img[0], "rb")
    # return image
    return StreamingResponse(file, media_type="image/" + img[1].lower())


@app.get("/json/")
async def json(type_filter: Union[str, None] = Query(default=None, max_length=10, regex=r"^(acg|wallpaper|avatar)$"),
               size: Union[str, None] = Query(default=None, max_length=10, regex=r"^([1-9]\d*|\?)x([1-9]\d*|\?)$")):
    print("type_filter: %s" % type_filter, "size: %s" % size)
    img_x = None
    img_y = None
    if size is not None:
        match_size = match(r"([1-9]\d*|\?)x([1-9]\d*|\?)", size)
        img_x = match_size.group(1)
        img_y = match_size.group(2)
    res = dbo.search(type=type_filter, img_x=img_x, img_y=img_y, needed="NAME, TYPE, IMG_X, IMG_Y")
    try:
        img = choice(res)
    except IndexError:
        return {"error": "no image found"}
    return [{"name": img[0], "type": img[1], "img_x": img[2], "img_y": img[3]}]
