import json
import os

from typing import Any

# If config directory doesn't exist, create it
if not os.path.exists("config"):
    os.mkdir("config")

# set the default config
default = {
        # download config
        "img_path": "img",
        "r18": 2,

        # database config
        "database_name": "img_info.sqlite3",

        # server config
        "log_level": "INFO"
    }


# If config file doesn't have a value, read it from the default config file
def get_default(key: str) -> Any:
    return default[key]


class Config:
    def __init__(self, config_file: str) -> None:
        """
        :param config_file: the name of the config file
        """
        # get config file path
        self.config_file = os.path.join("config", config_file)
        # if config file doesn't exist, create it
        try:
            with open(self.config_file, 'r', encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            with open(self.config_file, 'w', encoding="utf-8") as f:
                print("Config file not found, creating a new one.")
                json.dump({}, f, indent=4)
                self.config = {}

    def get(self, key: str) -> Any:
        """
        :param key: key to get from config
        :return: value of key, if key doesn't exist, return default value
        """
        try:
            return self.config[key]
        except KeyError:
            return get_default(key)

    def set(self, key: str, value: Any) -> None:
        """
        :param key: key to set
        :param value: value to set
        :return: error message if error occurs, else None
        """
        self.config[key] = value

    def save(self, config_file: str = None) -> None:
        """
        :param config_file: config file to save to, if None, save to self.config_file
        :return: error message if error occurs, else None
        """
        if config_file is None:
            config_file = self.config_file
        else:
            config_file = os.path.join("config", config_file)
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)
