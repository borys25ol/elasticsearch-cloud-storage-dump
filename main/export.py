import os
import tempfile
from functools import singledispatchmethod
from typing import Any, Dict, List

import pandas as pd
from google.cloud import storage

from main.client import get_elasticsearch_client
from main.config import CLOUD_STORAGE_BUCKET, GOOGLE_CREDENTIAL_PATH
from main.const import (
    GOOGLE_ENV_KEY,
    CSVFormat,
    ExcelFormat,
    ExportFormat,
    ExportType,
    JSONFormat,
)

os.environ[GOOGLE_ENV_KEY] = str(GOOGLE_CREDENTIAL_PATH)


class GoogleCloudExportService:
    """
    Service for exporting data from Elasticsearch storage.
    """

    file_format_to_type_map: Dict[str, Any] = {
        ExportFormat.csv: CSVFormat(),
        ExportFormat.json: JSONFormat(),
        ExportFormat.xlsx: ExcelFormat(),
    }

    def __init__(self) -> None:
        self.es_client = get_elasticsearch_client()
        self._storage_client = storage.Client()
        self._bucket = self._storage_client.get_bucket(
            bucket_or_name=CLOUD_STORAGE_BUCKET
        )

    def export_data_to_cloud_storage(self, es_index: str, file_format: str) -> None:
        """
        Load data from Elasticsearch index and upload to Google Cloud Storage.
        """
        data = self.es_client.load_data_from_index(es_index=es_index)
        self._upload_data_to_cloud_storage(
            file_name=es_index, data=data, file_format=file_format
        )

    def _upload_data_to_cloud_storage(
        self, file_name: str, data: List[dict], file_format: str
    ) -> str:
        """
        Upload exported data to Google Cloud Storage.
        """
        blob = self._bucket.blob(blob_name=f"{file_name}.{file_format}")
        format_class = self._get_format_class(file_format=file_format)
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = self._export_data_to_specific_format(
                format_class, data=data, file_name=file_name, temp_dir=temp_dir
            )
            blob.upload_from_filename(filename=file_name)
        return blob.public_url

    def _get_format_class(self, file_format: str) -> str:
        """
        Check if file format is valid and if tool can handle export.
        """
        format_class = self.file_format_to_type_map.get(file_format)
        if not format_class:
            raise ValueError("Invalid file format")
        return format_class

    @singledispatchmethod
    def _export_data_to_specific_format(
        self, format_class: ExportType, data: List[dict], file_name: str, temp_dir: str
    ) -> str:
        """
        Main function for registration new export file format functions.
        """
        raise NotImplementedError(f"Not implemented type: {type(format_class)}")

    @_export_data_to_specific_format.register
    def _export_data_to_csv(
        self, format_class: CSVFormat, data: List[dict], file_name: str, temp_dir: str
    ) -> str:
        """
        Export data to CSV format.
        """
        df = pd.DataFrame(data=data)
        file_name = f"{temp_dir}/{file_name}.{format_class.file_format}"
        df.to_csv(path_or_buf=file_name, index=False)
        return file_name

    @_export_data_to_specific_format.register
    def _export_data_to_json(
        self, format_class: JSONFormat, data: List[dict], file_name: str, temp_dir: str
    ) -> str:
        """
        Export data to JSON format.
        """
        df = pd.DataFrame(data=data)
        file_name = f"{temp_dir}/{file_name}.{format_class.file_format}"
        df.to_json(path_or_buf=file_name, orient="records", force_ascii=False, indent=4)
        return file_name

    @_export_data_to_specific_format.register
    def _export_data_to_excel(
        self, format_class: ExcelFormat, data: List[dict], file_name: str, temp_dir: str
    ) -> str:
        """
        Export data to EXCEL format.
        """
        df = pd.DataFrame(data=data)
        file_name = f"{temp_dir}/{file_name}.{format_class.file_format}"
        df.to_excel(excel_writer=file_name, index=False)
        return file_name
