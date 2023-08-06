"""
A logger that gets dumped to stdout when closed
"""

import inspect
import logging
import os
from logging.handlers import MemoryHandler
from typing import Any, Optional


class MemoryLogger:
    """
    A logger that gets dumped to stdout when closed
    """

    def __init__(
        self,
        file_name: str,
        lock: Optional[Any],
        log_name: Optional[str] = None,
        flush_immed: bool = False,
    ) -> None:
        self.flush_immed = flush_immed
        self.lock = lock

        if log_name is None:
            caller = inspect.stack()[1][0].f_locals["self"].__class__.__name__
            log_name = f"{caller}--{os.getpid()}"

        self._logger = logging.getLogger(log_name)

        self._logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)

        log_handler = MemoryHandler(
            10000, flushLevel=logging.CRITICAL, target=file_handler
        )
        log_handler.setFormatter(formatter)
        self._logger.addHandler(log_handler)

    def flush(self) -> None:
        """
        Flush all handlers for this logger
        """
        if self.lock is not None:
            with self.lock:
                for handler in self._logger.handlers:
                    handler.flush()
        else:
            for handler in self._logger.handlers:
                handler.flush()

    def close(self) -> None:
        """
        Close (and flush) all handlers for this logger
        """
        if self.lock is not None:
            with self.lock:
                for handler in self._logger.handlers:
                    handler.close()
        else:
            for handler in self._logger.handlers:
                handler.close()

    def clear_targets(self) -> None:
        """
        Makes the target for all Memory Handlers in this logger None

        Thus when these handlers are flushed, nothing will go to standard output
        """
        for handler in self._logger.handlers:
            if isinstance(handler, MemoryHandler):
                handler.setTarget(None)

    def log(self, level: int, msg: str) -> None:
        """
        Wrapper function for logging messages
        """
        self._logger.log(level, msg)
        if self.flush_immed:
            self.flush()

    def debug(self, msg: str) -> None:
        """
        Wrapper function for debug messages
        """
        self.log(logging.DEBUG, msg)

    def info(self, msg: str) -> None:
        """
        Wrapper function for info messages
        """
        self.log(logging.INFO, msg)

    def warning(self, msg: str) -> None:
        """
        Wrapper function for warn messages
        """
        self.log(logging.WARNING, msg)

    def error(self, msg: str) -> None:
        """
        Wrapper function for error messages
        """
        self.log(logging.ERROR, msg)

    def fatal(self, msg: str) -> None:
        """
        Wrapper function for fatal messages
        """
        self.log(logging.FATAL, msg)

    def critical(self, msg: str) -> None:
        """
        Wrapper function for critical messages
        """
        self.log(logging.CRITICAL, msg)
