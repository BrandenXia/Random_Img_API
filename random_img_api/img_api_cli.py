import rich_click as click

from random_img_api.src.get_img.get_img import get
from random_img_api.src.run import run


@click.group()
@click.version_option(version="v1.1.1")
def cli():
    """
    Random Image API command line interface
    """
    pass


# Add commands
cli.add_command(get)
cli.add_command(run)
