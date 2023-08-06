import json
from typing import Any

from .types import EnvironmentIdentifier
from .types import MeroxaApiResponse
from .utils import api_response
from .utils import ComplexEncoder

RESOURCE_BASE_PATH = "/v1/resources"


class Status(object):
    def __init__(
        self,
        state: str,
        details: str = None,
        last_updated_at: str = None,
    ) -> None:
        self.state = state
        self.details = details
        self.last_updated_at = last_updated_at


class ResourcesResponse(MeroxaApiResponse):
    def __init__(
        self,
        uuid: str,
        name: str,
        type: str,
        url: str,
        metadata: dict,
        connector_count: int,
        status: Any,
        created_at: str,
        updated_at: str,
        **kwargs
    ) -> None:
        self.uuid = uuid
        self.name = name
        self.type = type
        self.url = url
        self.metadata = metadata
        self.connector_count = connector_count
        self.status = Status(**status)
        self.created_at = created_at
        self.updated_at = updated_at
        super().__init__()


class ResourceCredentials:
    def __init__(
        self,
        username: str,
        password: str,
        ca_cert: str,
        client_cert: str,
        client_cert_key: str,
        ssl: bool,
    ):
        self._username = username
        self._password = password
        self._ca_cert = ca_cert
        self._client_cert = client_cert
        self._client_cert_key = client_cert_key
        self._ssl = ssl

    def repr_json(self):
        return dict(
            username=self._username,
            password=self._password,
            ca_cert=self._ca_cert,
            client_cert=self._client_cert,
            client_cert_key=self._client_cert_key,
            ssl=self._ssl,
        )


class ResourceSSHTunnel:
    def __init__(self, address: str, private_key: str):
        self._address = address
        self._private_key = private_key

    def repr_json(self):
        return dict(address=self.address, private_key=self.private_key)


class CreateResourceParams:
    def __init__(
        self,
        url: str,
        type: str,
        name: str = None,
        metadata: dict[str, str] = None,
        credentials: ResourceCredentials = None,
        environment: EnvironmentIdentifier = None,
        ssh_tunnel: ResourceSSHTunnel = None,
    ) -> None:
        self._url = url
        self._type = type
        self._name = name
        self._credentials = credentials
        self._metadata = metadata
        self._environment = environment
        self._ssh_tunnel = ssh_tunnel

    def repr_json(self):
        return dict(
            name=self._name,
            url=self._url,
            credentials=self._credentials,
            environment=self._environment,
            metadata=self._metadata,
            type=self._type,
            ssh_tunnel=self._ssh_tunnel,
        )


class UpdateResourceParams:
    def __init__(
        self,
        name: str,
        url: str,
        credentials: ResourceCredentials = None,
        metadata: dict[str, str] = None,
        ssh_tunnel: ResourceSSHTunnel = None,
    ) -> None:
        self._name = name
        self._url = url
        self._credentials = credentials
        self._metadata = metadata
        self._ssh_tunnel = ssh_tunnel

    def repr_json(self):
        return dict(
            name=self._name,
            url=self._url,
            credentials=self._credentials,
            metadata=self._metadata,
            ssh_tunnel=self._ssh_tunnel,
        )


class Resources:
    def __init__(self, session) -> None:
        self._session = session

    @api_response(ResourcesResponse)
    async def get(self, name_or_id: str):
        async with self._session.get(
            RESOURCE_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.text()

    @api_response(ResourcesResponse)
    async def list(self):
        async with self._session.get(RESOURCE_BASE_PATH) as resp:
            return await resp.text()

    async def delete(self, name_or_id: str):
        async with self._session.delete(
            RESOURCE_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.text()

    @api_response(ResourcesResponse)
    async def create(self, create_resource_parameters: CreateResourceParams):
        async with self._session.post(
            RESOURCE_BASE_PATH,
            data=json.dumps(create_resource_parameters.repr_json(), cls=ComplexEncoder),
        ) as resp:
            return await resp.text()

    @api_response(ResourcesResponse)
    async def update(
        self, name_or_id: str, update_resource_parameters: UpdateResourceParams
    ):
        async with self._session.post(
            RESOURCE_BASE_PATH + "/{}".format(name_or_id),
            json=json.dumps(update_resource_parameters.repr_json(), cls=ComplexEncoder),
        ) as resp:
            res = await resp.text()
            return ResourcesResponse(**json.loads(res))
