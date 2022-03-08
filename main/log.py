"""
Module configuration custom logger.
"""
import logging
from typing import Optional

from main.config import DEFAULT_LOGGER_NAME, LOG_MESSAGE_FORMAT


class ProjectLogger:
    """
    Custom project logger.
    """

    def __init__(self, name: str):
        self.name = name
        self._logger: Optional[logging.Logger] = None

    def __call__(self, *args: tuple, **kwargs: dict) -> logging.Logger:
        return self.logger

    @property
    def logger(self) -> logging.Logger:
        """
        Return initialized logger object.
        """
        if not self._logger:
            self._logger = self.create_logger()
        return self._logger

    def create_logger(self) -> logging.Logger:
        """
        Return configured logger.
        """
        logging.basicConfig(format=LOG_MESSAGE_FORMAT)

        project_logger = logging.getLogger(name=self.name)
        project_logger.setLevel(level=logging.INFO)

        return project_logger


def _create_logger() -> logging.Logger:
    """
    Initialize logger for project.
    """
    return ProjectLogger(name=DEFAULT_LOGGER_NAME)()


logger = _create_logger()
