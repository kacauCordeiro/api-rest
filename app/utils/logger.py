"""Logger."""
import json
import logging
import os
import sys
from uuid import uuid4


class Logger:  # pragma: no cover
    """Logger class."""

    def __init__(self, name=os.environ.get("PROJECT_NAME", "log-default"), uuid=None):
        """Class constructor."""
        if uuid is None:
            if not os.environ.get("LOGGER_UUID", ""):
                self.set_uuid()
            self.uuid = os.environ.get("LOGGER_UUID", uuid4())

        self._logger = logging.getLogger(name)
        log_format = json.dumps(
            {
                "uuid": f"{uuid if uuid else self.uuid}",
                "timestamp": "%(asctime)s",
                "log_level": "%(levelno)s",
                "project_name": f"{name}",
                "message": "%(message)s",
            }
        )
        formatter = logging.Formatter(log_format)
        hdlr = logging.StreamHandler(sys.stdout)
        hdlr.setFormatter(formatter)
        self._logger.handlers.clear()
        self._logger.addHandler(hdlr)
        self._logger.setLevel(int(os.environ.get("LOG_LEVEL", logging.INFO)))

    @staticmethod
    def uuid(unique_identifier=None):  # pylint: disable=E0202
        """Decorate que altera o identificador unico da classe Logger.

        Args:
            unique_identifier (Any, optional): Codigo a ser apresentado nas mensagens de log. Defaults to None.
        """

        def decorator(function):
            def wrapper(*args, **kwargs):
                Logger.set_uuid(unique_identifier)
                return function(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def set_uuid(unique_identifier=None):
        """Adiciona um identificador unico as mensagens de log.

        Args:
            unique_identifier (_type_, optional): _description_. Defaults to None.
        """
        if unique_identifier is None:
            unique_identifier = uuid4()
        if not isinstance(unique_identifier, str):
            uuid = str(unique_identifier)
        os.environ["LOGGER_UUID"] = uuid

    def info(self, message, *args, **kwargs):
        """Log info."""
        self._logger.info(message, *args, **kwargs)

    def success(self, message, *args, **kwargs):
        """Log success."""
        self._logger.info(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """Log error."""
        self._logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """Log critical."""
        self._logger.critical(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        """Log debug."""
        self._logger.debug(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """Log warning."""
        self._logger.warning(message, *args, **kwargs)
