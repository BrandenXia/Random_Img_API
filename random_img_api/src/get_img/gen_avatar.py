import time
import os
import pydenticon

from rich.console import Console

from random_img_api.src.config import config

console = Console()

_config = config.Config("config.json")
img_path = _config.get("img_path")


def gen_avatar() -> str:
    seed = str(time.time_ns())

    foreground = ["rgb(45,79,255)",
                  "rgb(254,180,44)",
                  "rgb(226,121,234)",
                  "rgb(30,179,253)",
                  "rgb(232,77,65)",
                  "rgb(49,203,115)",
                  "rgb(141,69,170)"]

    # Set-up a background colour.
    background = "rgb(224,224,224)"

    # Set up the padding (top, bottom, left, right) in pixels.
    padding = (20, 20, 20, 20)

    # Generate a PNG image using a generator that will create 10x10 block identicons using SHA1 digest.
    identicon = pydenticon.Generator(10, 10, foreground=foreground,
                                     background=background).generate(seed, 200, 200,
                                                                     padding=padding,
                                                                     output_format="png")

    filename = "avatar-%s.png" % seed
    with open(os.path.join(img_path, filename), "wb") as write_avatar:
        write_avatar.write(identicon)

    console.log("[cyan][bold]%s[/bold] generated[/cyan]" % filename)

    return filename
