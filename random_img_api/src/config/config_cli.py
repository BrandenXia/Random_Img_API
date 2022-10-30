import rich_click as click

from rich.console import Console

from random_img_api.src.config import config
from random_img_api.src.config.config import default

console = Console()
# get config
_config = config.Config("config.json")


def setup_config(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    # ask if user wants to continue
    console.print("[bold red]Are you sure you want to continue? This action might override current config.", end="")
    continue_prog = click.confirm("")
    # if not, exit
    if not continue_prog:
        console.print("[bold cyan]Setup canceled")
        ctx.exit()
    # get all key from default config
    for key in default:
        # ask for value
        console.print("Enter [blue]%s[/blue] value" % key, end="")
        value = click.prompt("", default=None)
        # if value is not None, set it
        if value is not None:
            _config.set(key, value)
            console.print("Set [green]%s[/green] to [yellow]%s[/yellow]" % (key, value,))
    # save config
    _config.save()
    console.print("[bold green]Setup completed")
    # exit
    ctx.exit()


@click.command()
@click.argument("config_value", nargs=-1, type=str, required=True)
@click.option("--setup", "-s", is_flag=True, callback=setup_config,
              expose_value=False, is_eager=True, help="Setup config file")
def config(config_value: str):
    """Configure the application."""
    for i in config_value:
        # try to split the config value
        try:
            key, value = i.split("=")
        # if not able to split, set value to None and show current config
        except ValueError:
            key = i
            value = None
        if key in default:
            # if not able to split, show current config
            if value is None:
                console.print("Current [green]%s[/green] value is [yellow]%s[/yellow]" % (i, _config.get(i),))
            else:
                # set value
                _config.set(key, value)
                console.print("Set [green]%s[/green] to [yellow]%s[/yellow]" % (key, value,))
                # save config
                _config.save()
                console.print("[bold green]Config saved")
        else:
            # if key not in default config, show error message
            console.print("[bold red]Invalid key: %s" % key)
