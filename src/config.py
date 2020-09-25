"""Import config from config.ini file."""

import configparser

config = configparser.ConfigParser()
config.optionxform = str
config.read('config.ini')
CONFIG = {s: dict(config.items(s)) for s in config.sections()}
