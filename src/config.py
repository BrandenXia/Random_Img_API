import json
import os

# If config directory doesn't exist, create it
if not os.path.exists("config"):
    os.mkdir("config")


# If config file doesn't have a value, read it from the default config file
def get_default(key):
    with open("default.json", "r", encoding="utf-8") as f:
        default = json.load(f)
    return default[key]


class Config:
    def __init__(self, config_file):
        self.config_file = os.path.join("config", config_file)
        try:
            with open(self.config_file, 'r', encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            with open(self.config_file, 'w', encoding="utf-8") as f:
                print("Config file not found, creating a new one.")
                json.dump({}, f, indent=4)
                self.config = {}

    def get(self, key):
        try:
            return self.config[key]
        except KeyError:
            return get_default(key)

    def set(self, key, value):
        self.config[key] = value

    def save(self, config_file=None):
        if config_file is None:
            config_file = self.config_file
        config_file = os.path.join("config", config_file)
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)
