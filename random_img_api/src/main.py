from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from re import compile
from random import choice

from random_img_api.src import dbo

# init app
app = FastAPI()
# init database
dbo.init()
# compile regex
match_size = compile(r"([1-9]\d*|\?)x([1-9]\d*|\?)")


# app routes
@app.get("/")
async def main(type: str | None = Query(default=None, max_length=10, regex=r"^(acg|wallpaper|avatar)$"),
               size: str | None = Query(default=None, max_length=10, regex=r"^([1-9]\d*|\?)x([1-9]\d*|\?)$"),
               rt: str = Query(default="img", max_length=10, regex=r"(json|img)")
               ) -> StreamingResponse or dict:
    """
    :param type: type of image (acg / wallpaper / avatar)
    :param size: size of image (width x height)
    :param rt: return type (json / img)
    :return: error message if error occurred, else image
    """
    img_x = None
    img_y = None
    # if size is not None, split it
    if size is not None:
        img_size = match_size.match(size)
        img_x = img_size.group(1)
        img_y = img_size.group(2)
    # get image from database
    res = dbo.search(type=type, img_x=img_x, img_y=img_y, needed="PATH,FORMAT")

    try:
        # get random image
        img = choice(res)
    # if no image found, return error message
    except IndexError:
        return {"error": "no image found"}

    # if return type is img, return img
    if rt == "img":
        file = open(img[0], "rb")
        # return image
        return StreamingResponse(file, media_type="image/" + img[1].lower())
    # if return type is json, return json
    elif rt == "json":
        return {"name": img[0], "type": img[1], "img_x": img[2], "img_y": img[3]}
