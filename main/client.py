from typing import List, Optional

from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import scan

from main.config import (
    ELASTICSEARCH_HOST,
    ELASTICSEARCH_PASSWORD,
    ELASTICSEARCH_PORT,
    ELASTICSEARCH_USERNAME,
)
from main.log import logger


class ElasticsearchClient:
    """
    Client for retrieving data from Elasticsearch collection.
    """

    def __init__(
        self,
        host: str,
        port: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    @property
    def connection(self) -> Elasticsearch:
        """
        Return connection to Elasticsearch server.
        """
        return self._get_elasticsearch_client()

    def _get_elasticsearch_client(self) -> Elasticsearch:
        """
        Check connection to Elasticsearch and return client.
        """
        elastic_kwargs = {"hosts": [{"host": self.host, "port": int(self.port)}]}
        if self.username and self.password:
            elastic_kwargs.update({"http_auth": (username, password)})  # type: ignore

        client = Elasticsearch(**elastic_kwargs)  # type: ignore
        try:
            client.info()
        except exceptions.ConnectionError:
            raise ValueError(f"Can not connect to ElasticSearch server: {self.host}")

        logger.debug(f"Successfully connected to server: {self.host}")

        return client

    def load_data_from_index(self, es_index: str) -> List[dict]:
        """
        Retrieve all data from Elasticsearch `es_index` collection.
        """
        query: dict = {"query": {"match_all": {}}}
        return [
            item["_source"]
            for item in scan(client=self.connection, query=query, index=es_index)
        ]


def get_elasticsearch_client() -> ElasticsearchClient:
    """
    Return initialized Elasticsearch client.
    """
    return ElasticsearchClient(
        host=ELASTICSEARCH_HOST,
        port=ELASTICSEARCH_PORT,
        username=ELASTICSEARCH_USERNAME,
        password=ELASTICSEARCH_PASSWORD,
    )
