from enum import Enum
from typing import Any


class ResourceType(Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    REDSHIFT = "redshift"
    URL = "url"
    S3 = "s3"
    MONGODB = "mongodb"
    ELASTICSEARCH = "elasticsearch"
    SNOWFLAKE = "snowflakedb"
    BIGQUERY = "bigquery"
    SQLSERVER = "sqlserver"
    COSMODB = "cosmodb"
    KAFKA = "kafka"
    CONFLUENTCLOUD = "confluentcloud"


class MeroxaApiResponse(object):
    def __init__(self, *args, **kwargs):
        ...


class ClientOptions:
    def __init__(self, auth: str, url: str, timeout=0.0):
        self.auth = auth
        self.timeout = timeout
        self.url = url


class EnvironmentIdentifier:
    def __init__(self, name=None, uuid=None):
        self.name = name
        self.uuid = uuid

    def repr_json(self):
        return dict(name=self.name) if self.name is not None else dict(uuid=self.uuid)


class ResourceCollection:
    def __init__(self, name=None, destination=None, source=None):

        self.name = name
        self.source = source
        self.destination = destination


class ApplicationResource:
    def __init__(self, name=None, uuid=None, collection: Any = None):

        self.name = name
        self.uuid = uuid
        self.collection = ResourceCollection(**collection)


class EntityIdentifier:
    def __init__(self, name=None, uuid=None):
        self.name = name
        self.uuid = uuid

    def repr_json(self):
        return dict(name=self.name) if self.name is not None else dict(uuid=self.uuid)
