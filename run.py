import multiprocessing
import os

from gunicorn.app.base import BaseApplication

from main import app


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in self.options.items()
                       if key in self.cfg.settings and value is not None])
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.mkdir('logs')

    options = {
        "bind": "0.0.0.0:8045",
        "workers": multiprocessing.cpu_count() * 2 + 1,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "threads": 2,
        "timeout": 120,
        "workers_connections": 1000,
        "accesslog": "-",
        "errorlog": "-",
        "logconfig_dict": {
            "level": "INFO",
            "format": '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"',
        },
        "preload_app": True
    }

    StandaloneApplication(app, options).run()
