import rich_click as click

from src.get_img.get_img import get
from src.run import run


@click.group()
@click.version_option(version="v1.1")
def cli():
    """
    Random Image API command line interface
    """
    pass


cli.add_command(get)
cli.add_command(run)
