import logging
import rich_click as click

from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger
from multiprocessing import cpu_count
from rich.logging import RichHandler

from random_img_api.src.main import app
from random_img_api.src.config import config


class StubbedGunicornLogger(Logger):
    """
    logger class for app
    """
    def __init__(self, cfg):
        super().__init__(cfg)
        self.access_logger = None
        self.error_logger = None

    def setup(self, cfg) -> None:
        """
        :param cfg: the configuration
        :return: None
        """
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_logger.setLevel(logging.INFO)
        self.access_logger.setLevel(logging.INFO)


class StandaloneApplication(BaseApplication):
    """
    Standalone gunicorn application
    """

    def __init__(self, app, options=None) -> None:
        """
        :param app: the app
        :param options: the running options
        """
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self) -> None:
        # get config
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


@click.command()
@click.option("--port", "-p", default=8045, type=int, metavar="PORT", help="Port to run on")
@click.option("--threads", "-t", default=2, type=int, help="Number of threads to run")
@click.option("--workers", "-w", default=cpu_count() * 2 + 1, type=int, help="Number of workers to run")
def run(port, threads, workers):
    """
    Run the random image server
    """
    # set log level
    _config = config.Config("config.json")
    log_level = _config.get("log_level")

    # set log format and log handler
    intercept_handler = RichHandler(rich_tracebacks=True)
    logging.basicConfig(handlers=[intercept_handler], level=log_level, format='%(message)s')
    logging.root.handlers = [intercept_handler]
    logging.root.setLevel(logging.INFO)

    # log handler
    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]

    # set gunicorn options
    options = {
        "bind": "0.0.0.0:%d" % port,
        "workers": workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "threads": threads,
        "timeout": 120,
        "workers_connections": 1000,
        "accesslog": "-",
        "errorlog": "-",
        "logger_class": StubbedGunicornLogger,
        "preload_app": True
    }

    # run app
    StandaloneApplication(app, options).run()
