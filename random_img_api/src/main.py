from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from typing import Union
from re import match
from random import choice

from random_img_api.src import dbo

# init app
app = FastAPI()
# init database
dbo.init()


# app routes
@app.get("/")
async def main(type: Union[str, None] = Query(default=None, max_length=10, regex=r"^(acg|wallpaper|avatar)$"),
               size: Union[str, None] = Query(default=None, max_length=10, regex=r"^([1-9]\d*|\?)x([1-9]\d*|\?)$")
               ) -> StreamingResponse or dict:
    """
    :param type: type of image (acg / wallpaper / avatar)
    :param size: size of image (width x height)
    :return: error message if error occurred, else image
    """
    img_x = None
    img_y = None
    # if size is not None, split it
    if size is not None:
        match_size = match(r"([1-9]\d*|\?)x([1-9]\d*|\?)", size)
        img_x = match_size.group(1)
        img_y = match_size.group(2)
    # get image from database
    res = dbo.search(type=type, img_x=img_x, img_y=img_y, needed="PATH,FORMAT")

    try:
        # get random image
        img = choice(res)
    # if no image found, return error message
    except IndexError:
        return {"error": "no image found"}
    file = open(img[0], "rb")

    # return image
    return StreamingResponse(file, media_type="image/" + img[1].lower())


@app.get("/json/")
async def json(type: Union[str, None] = Query(default=None, max_length=10, regex=r"^(acg|wallpaper|avatar)$"),
               size: Union[str, None] = Query(default=None, max_length=10, regex=r"^([1-9]\d*|\?)x([1-9]\d*|\?)$")
               ) -> dict:
    """
    :param type: type of image (acg / wallpaper / avatar)
    :param size: size of image (width x height)
    :return: error message if error occurred, else json
    """
    img_x = None
    img_y = None
    # if size is not None, split it
    if size is not None:
        match_size = match(r"([1-9]\d*|\?)x([1-9]\d*|\?)", size)
        img_x = match_size.group(1)
        img_y = match_size.group(2)
    # get image from database
    res = dbo.search(type=type, img_x=img_x, img_y=img_y, needed="NAME, TYPE, IMG_X, IMG_Y")

    try:
        # get random image
        img = choice(res)
    # if no image found, return error message
    except IndexError:
        return {"error": "no image found"}

    # return json
    return {"name": img[0], "type": img[1], "img_x": img[2], "img_y": img[3]}
