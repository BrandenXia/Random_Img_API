import rich_click as click

from rich.traceback import install

from random_img_api.src.get_img.get_img import get
from random_img_api.src.run import run
from random_img_api.src.config.config_cli import config

install(show_locals=True)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option()
def cli():
    """
    Random Image API command line interface
    """
    pass


# Add commands
cli.add_command(get)
cli.add_command(run)
cli.add_command(config)

