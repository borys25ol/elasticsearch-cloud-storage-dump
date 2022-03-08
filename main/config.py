import os
from pathlib import Path

GOOGLE_CREDENTIAL_PATH = Path(__file__).parent.parent / "google_credentials.json"

CLOUD_STORAGE_BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]

ELASTICSEARCH_HOST = os.environ["ELASTICSEARCH_HOST"]
ELASTICSEARCH_PORT = os.environ["ELASTICSEARCH_PORT"]
ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")

# Logs format for project logger.
LOG_MESSAGE_FORMAT = "[%(name)s] [%(asctime)s] %(message)s"

DEFAULT_LOGGER_NAME = "cloud-storage-dump"
