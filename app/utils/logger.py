"""
Sentinel-AI — Structured Logger
Colored console output with log levels.
"""

import sys
from datetime import datetime, timezone


class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"


class Logger:
    def __init__(self, name: str = "sentinel"):
        self.name = name

    def _log(self, level: str, color: str, message: str, **kwargs):
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        prefix = f"{Colors.GRAY}{ts}{Colors.RESET} {color}{Colors.BOLD}[{level}]{Colors.RESET} {Colors.CYAN}{self.name}{Colors.RESET}"
        extra = ""
        if kwargs:
            extra = " " + " ".join(f"{Colors.GRAY}{k}={Colors.RESET}{v}" for k, v in kwargs.items())
        print(f"{prefix} {message}{extra}", file=sys.stderr)

    def info(self, message: str, **kwargs):
        self._log("INFO", Colors.GREEN, message, **kwargs)

    def warn(self, message: str, **kwargs):
        self._log("WARN", Colors.YELLOW, message, **kwargs)

    def error(self, message: str, **kwargs):
        self._log("ERROR", Colors.RED, message, **kwargs)

    def debug(self, message: str, **kwargs):
        self._log("DEBUG", Colors.BLUE, message, **kwargs)

    def threat(self, message: str, **kwargs):
        self._log("THREAT", Colors.MAGENTA, message, **kwargs)


log = Logger()
