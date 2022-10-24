import logging
import multiprocessing
import os

from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger
from rich.logging import RichHandler

from main import app


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_logger.setLevel(logging.INFO)
        self.access_logger.setLevel(logging.INFO)


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.mkdir('logs')

    intercept_handler = RichHandler(rich_tracebacks=True)
    logging.basicConfig(handlers=[intercept_handler], level=logging.INFO)
    logging.root.handlers = [intercept_handler]
    logging.root.setLevel(logging.INFO)

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

    options = {
        "bind": "0.0.0.0:8045",
        "workers": multiprocessing.cpu_count() * 2 + 1,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "threads": 2,
        "timeout": 120,
        "workers_connections": 1000,
        "accesslog": "-",
        "errorlog": "-",
        "logger_class": StubbedGunicornLogger,
        "preload_app": True
    }

    StandaloneApplication(app, options).run()
