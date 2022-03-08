from dataclasses import dataclass
from enum import Enum
from typing import Union

# Environment variable for gcloud service credentials.
GOOGLE_ENV_KEY = "GOOGLE_APPLICATION_CREDENTIALS"


class ExportFormat(str, Enum):
    """
    Available formats to export.
    """

    csv = "csv"
    json = "json"
    xlsx = "xlsx"


AVAILABLE_FORMATS = list(ExportFormat)


@dataclass
class CSVFormat:
    file_format: str = ExportFormat.csv


@dataclass
class JSONFormat:
    file_format: str = ExportFormat.json


@dataclass
class ExcelFormat:
    file_format: str = ExportFormat.xlsx


ExportType = Union[CSVFormat, JSONFormat, ExcelFormat]
