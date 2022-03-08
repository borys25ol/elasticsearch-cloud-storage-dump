Elasticsearch GCP Cloud Storage Dump Tool
====================

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pre-commit: enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat)](https://github.com/pre-commit/pre-commit)

This tool can be used for simple exporting data from Elasticsearch collections to Google Cloud Storage Bucket in popular file formats.

Available formats:
* CSV
* JSON
* XLSX (Excel)

Developing
-----------

Install pre-commit hooks to ensure code quality checks and style checks


    $ make install_hooks

Then see `Configuration` section

You can also use these commands during dev process:

- to run mypy checks


      $ make types

Configuration
--------------

Replace `.env.example` with real `.env`, changing placeholders

```
CLOUD_STORAGE_BUCKET=<test-cloud-storage-bucket>

ELASTICSEARCH_HOST=<es-host>
ELASTICSEARCH_PORT=<es-port>
ELASTICSEARCH_USERNAME=<es-username|optional>
ELASTICSEARCH_PASSWORD=<es-password|optional>
```

Local install
-------------

Setup and activate a python3 virtualenv via your preferred method. e.g. and install production requirements:


    $ make ve

For remove virtualenv:


    $ make clean


Local run
-------------
Export path to Environment Variables:


    $ export PYTHONPATH='.'

Add file with GCP credentials to project root folder.

File should be similar with `google_credentials.example.json`

Code Example
-------------
```python
from main.const import AVAILABLE_FORMATS
from main.export import GoogleCloudExportService


def main():
    service = GoogleCloudExportService()
    for file_format in AVAILABLE_FORMATS:
        print(f"Export data to {file_format}:")
        service.export_data_to_cloud_storage(
            es_index="test-es-index", file_format=file_format
        )
        print("Export finished")


if __name__ == "__main__":
    main()

```
