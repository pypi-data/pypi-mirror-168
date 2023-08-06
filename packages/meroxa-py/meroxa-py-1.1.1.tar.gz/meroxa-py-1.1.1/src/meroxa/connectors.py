import json
from typing import Any

from .types import EntityIdentifier
from .types import MeroxaApiResponse
from .utils import api_response
from .utils import ComplexEncoder

CONNECTORS_BASE_PATH = "/v1/connectors"


class ConnectorsResponse(MeroxaApiResponse):
    def __init__(
        self,
        id: str,
        config: dict[str, str],
        created_at: str,
        metadata: dict[str, str],
        name: str,
        resource_name: str,
        pipeline_name: str,
        resource_id: str,
        pipeline_id: str,
        streams: dict[str, str],
        state: str,
        type: str,
        updated_at: str,
        uuid: str,
        trace: str = None,
        environment: EntityIdentifier = None,
    ) -> None:
        self.id = id
        self.config = config
        self.created_at = created_at
        self.metadata = metadata
        self.name = name
        self.resource_name = resource_name
        self.pipeline_name = pipeline_name
        self.resource_id = resource_id
        self.pipeline_id = pipeline_id
        self.streams = streams
        self.state = state
        self.type = type
        self.updated_at = updated_at
        self.uuid = uuid
        self.trace = trace
        self.environment = environment
        super().__init__()


class CreateConnectorParams:
    def __init__(
        self,
        resource_name: str,
        pipeline_name: str,
        name: str = None,
        config: dict[str, str] = None,
        metadata: dict[str, str] = None,
        connector_type: str = None,
        input: str = None,
    ) -> None:
        self._resource_name = resource_name
        self._pipeline_name = pipeline_name
        self._name = name
        self._config = config
        self._metadata = metadata
        self._connector_type = connector_type
        self._input = input

    def repr_json(self):
        return dict(
            resource_name=self._resource_name,
            pipeline_name=self._pipeline_name,
            name=self._name,
            config=self._config,
            metadata=self._metadata,
            connector_type=self._connector_type,
            input=self._input,
        )


class UpdateConnectorParams:
    def __init__(
        self,
        name: str = None,
        config: dict[str, Any] = None,
    ) -> None:
        self._name = name
        self._config = config

    def repr_json(self):
        return dict(
            config=self._config,
            name=self._name,
        )


class Connectors:
    def __init__(self, session) -> None:
        self._session = session

    @api_response(ConnectorsResponse)
    async def get(self, name_or_id: str):
        async with self._session.get(
            CONNECTORS_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.text()

    @api_response(ConnectorsResponse)
    async def list(self):
        async with self._session.get(CONNECTORS_BASE_PATH) as resp:
            return await resp.text()

    async def delete(self, name_or_id: str):
        async with self._session.delete(
            CONNECTORS_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.text()

    @api_response(ConnectorsResponse)
    async def create(self, create_connector_parameters: CreateConnectorParams):
        async with self._session.post(
            CONNECTORS_BASE_PATH,
            data=json.dumps(
                create_connector_parameters.repr_json(), cls=ComplexEncoder
            ),
        ) as resp:
            return await resp.text()

    @api_response(ConnectorsResponse)
    async def update(
        self, name_or_id: str, update_connector_parameters: UpdateConnectorParams
    ):
        async with self._session.post(
            CONNECTORS_BASE_PATH + "/{}".format(name_or_id),
            json=json.dumps(
                update_connector_parameters.repr_json(), cls=ComplexEncoder
            ),
        ) as resp:
            return await resp.text()
