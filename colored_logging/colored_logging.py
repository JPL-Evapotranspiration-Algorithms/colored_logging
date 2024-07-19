import logging
import re
import sys
from os import makedirs
from os.path import expanduser, dirname
from typing import Union, Any

from termcolor import colored

# Default settings for stripping ANSI escape sequences
DEFAULT_STRIP_CONSOLE = False
DEFAULT_STRIP_FILE = True

# Default format and date format for logging messages
DEFAULT_FORMAT = "[%(asctime)s %(levelname)s] %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Color settings for different types of text
FILE = "blue"
DIR = "blue"
TIME = "green"
PLACE = "yellow"
VALUE = "cyan"
NAME = "yellow"

# Regular expression to match ANSI escape sequences
ANSI_ESCAPE = re.compile(r'\x1b[^m]*m')

def strip(text: str) -> str:
    """
    Strip ANSI escape sequences from the given text.

    Args:
        text (str): The text to strip.

    Returns:
        str: The stripped text.
    """
    return str(ANSI_ESCAPE.sub('', str(text)))

def URL(text: Union[str, Any]) -> str:
    """
    Color the given text as a URL.

    Args:
        text (Union[str, Any]): The text to color.

    Returns:
        str: The colored text.
    """
    return str(colored(str(text), FILE))

def file(text: Union[str, Any]) -> str:
    """
    Color the given text as a file.

    Args:
        text (Union[str, Any]): The text to color.

    Returns:
        str: The colored text.
    """
    return str(colored(str(text), FILE))

def dir(text: Union[str, Any]) -> str:
    """
    Color the given text as a directory.

    Args:
        text (Union[str, Any]): The text to color.

    Returns:
        str: The colored text.
    """
    return str(colored(str(text), DIR))

def time(text: Union[str, Any]) -> str:
    """
    Color the given text as time.

    Args:
        text (Union[str, Any]): The text to color.

    Returns:
        str: The colored text.
    """
    return str(colored(str(text), TIME))

def place(text: Union[str, Any]) -> str:
    """
    Color the given text as a place.

    Args:
        text (Union[str, Any]): The text to color.

    Returns:
        str: The colored text.
    """
    return str(colored(str(text), PLACE))

def val(text: Union[str, Any]) -> str:
    """
    Color the given text as a value.

    Args:
        text (Union[str, Any]): The text to color.

    Returns:
        str: The colored text.
    """
    return str(colored(str(text), VALUE))

def name(text: Union[str, Any]) -> str:
    """
    Color the given text as a name.

    Args:
        text (Union[str, Any]): The text to color.

    Returns:
        str: The colored text.
    """
    return str(colored(str(text), NAME))

class Formatter(logging.Formatter):
    """
    Custom logging formatter that supports stripping and coloring of log messages.
    """
    def __init__(
            self,
            *args,
            fmt: str = DEFAULT_FORMAT,
            datefmt: str = DEFAULT_DATE_FORMAT,
            strip: bool = DEFAULT_STRIP_CONSOLE,
            color: str = None,
            **kwargs):
        """
        Initialize the Formatter.

        Args:
            fmt (str): Log message format.
            datefmt (str): Date format.
            strip (bool): Whether to strip ANSI escape sequences.
            color (str): Color to apply to log messages.
        """
        super(Formatter, self).__init__(
            *args,
            fmt=fmt,
            datefmt=datefmt,
            **kwargs
        )

        self.strip = strip
        self.color = color

    def format(self, record) -> str:
        """
        Format the log record.

        Args:
            record: The log record to format.

        Returns:
            str: The formatted log message.
        """
        text = super(Formatter, self).format(record)

        if self.strip or self.color is not None:
            text = strip(text)

        if self.color is not None:
            text = colored(text, self.color)

        return text

def configure(
        filename: str = None,
        format: str = DEFAULT_FORMAT,
        datefmt: str = DEFAULT_DATE_FORMAT,
        strip_console: bool = DEFAULT_STRIP_CONSOLE,
        strip_file: bool = DEFAULT_STRIP_FILE):
    """
    Configure the logging system.

    Args:
        filename (str): The log file name.
        format (str): Log message format.
        datefmt (str): Date format.
        strip_console (bool): Whether to strip ANSI escape sequences in console output.
        strip_file (bool): Whether to strip ANSI escape sequences in file output.
    """
    if isinstance(filename, str) and filename.startswith("~"):
        filename = expanduser(filename)

    handlers = []

    class InfoFilter(logging.Filter):
        """
        Filter for INFO level log messages.
        """
        def filter(self, record):
            return record.levelno == logging.INFO

    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.INFO)
    info_handler.addFilter(InfoFilter())

    info_handler.setFormatter(Formatter(
        fmt=format,
        datefmt=datefmt,
        strip=strip_console
    ))

    handlers.append(info_handler)

    if filename is not None:
        makedirs(dirname(filename), exist_ok=True)

        info_file_handler = logging.FileHandler(
            filename=filename,
            mode="a"
        )

        info_file_handler.setLevel(logging.INFO)
        info_file_handler.addFilter(InfoFilter())

        info_file_handler.setFormatter(Formatter(
            fmt=format,
            datefmt=datefmt,
            strip=strip_file
        ))

        handlers.append(info_file_handler)

    class WarningFilter(logging.Filter):
        """
        Filter for WARNING level log messages.
        """
        def filter(self, record):
            return record.levelno == logging.WARNING

    warning_handler = logging.StreamHandler(sys.stdout)
    warning_handler.setLevel(logging.WARNING)
    warning_handler.addFilter(WarningFilter())

    warning_handler.setFormatter(Formatter(
        fmt=format,
        datefmt=datefmt,
        strip=strip_console,
        color="yellow"
    ))

    handlers.append(warning_handler)

    if filename is not None:
        warning_file_handler = logging.FileHandler(
            filename=filename,
            mode="a"
        )

        warning_file_handler.setLevel(logging.WARNING)
        warning_file_handler.addFilter(WarningFilter())

        warning_file_handler.setFormatter(Formatter(
            fmt=format,
            datefmt=datefmt,
            strip=strip_file
        ))

        handlers.append(warning_file_handler)

    class ErrorFilter(logging.Filter):
        """
        Filter for ERROR level log messages.
        """
        def filter(self, record):
            return record.levelno == logging.ERROR

    error_handler = logging.StreamHandler(sys.stdout)
    error_handler.setLevel(logging.ERROR)
    error_handler.addFilter(ErrorFilter())

    error_handler.setFormatter(Formatter(
        fmt=format,
        datefmt=datefmt,
        strip=strip_console,
        color="red"
    ))

    handlers.append(error_handler)

    if filename is not None:
        error_file_handler = logging.FileHandler(
            filename=filename,
            mode="a"
        )

        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.addFilter(ErrorFilter())

        error_file_handler.setFormatter(Formatter(
            fmt=format,
            datefmt=datefmt,
            strip=strip_file
        ))

        handlers.append(error_file_handler)

    while logging.root.hasHandlers():
        logging.root.removeHandler(logging.root.handlers[0])

    logging.basicConfig(
        level=logging.INFO,
        handlers=handlers
        # force=True
    )

configure()