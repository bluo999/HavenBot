"""Logger that outputs logs to stdout and keeps
a file log"""

import logging

from config import CONFIG


FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
)


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;1m"
    yellow = "\x1b[33;1m"
    red = "\x1b[31;1m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + FORMAT + reset,
        logging.INFO: grey + FORMAT + reset,
        logging.WARNING: yellow + FORMAT + reset,
        logging.ERROR: red + FORMAT + reset,
        logging.CRITICAL: bold_red + FORMAT + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


formatter = CustomFormatter()
logger = logging.getLogger()
logger.setLevel(CONFIG['Logging']['LogLevel'])

sh = logging.StreamHandler()
sh.setFormatter(formatter)

fh = logging.FileHandler(CONFIG['Logging']['LogFile'], mode='a', encoding='utf-8')
fh.setFormatter(logging.Formatter(FORMAT))

logger.addHandler(sh)
logger.addHandler(fh)
