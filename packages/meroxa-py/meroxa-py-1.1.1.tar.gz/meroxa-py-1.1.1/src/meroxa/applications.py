import json

from .pipelines import PipelineIdentifiers
from .types import ApplicationResource
from .types import EntityIdentifier
from .types import MeroxaApiResponse
from .utils import api_response
from .utils import ComplexEncoder

APPLICATIONS_BASE_PATH = "/v1/applications"


class ApplicationResponse(MeroxaApiResponse):
    def __init__(
        self,
        uuid: str,
        name: str,
        language: str,
        git_sha: str,
        status: dict,
        pipeline: dict,
        created_at: str,
        updated_at: str,
        connectors: list[EntityIdentifier] = None,
        functions: list[EntityIdentifier] = None,
        resources: list[ApplicationResource] = None,
    ) -> None:
        self.uuid = uuid
        self.name = name
        self.language = language
        self.git_sha = git_sha
        self.status = status
        self.pipeline = pipeline
        self.created_at = created_at
        self.updated_at = updated_at
        self.connectors = connectors
        self.functions = functions
        self.resources = resources
        super().__init__()


class CreateApplicationParams:
    def __init__(
        self,
        name: str,
        language: str,
        git_sha: str,
        pipeline: PipelineIdentifiers,
    ) -> None:
        self._name = name
        self._language = language
        self._git_sha = git_sha
        self._pipeline = pipeline

    def repr_json(self):
        return dict(
            name=self._name,
            language=self._language,
            git_sha=self._git_sha,
            pipeline=self._pipeline,
        )


class Applications:
    def __init__(self, session) -> None:
        self._session = session

    @api_response(ApplicationResponse)
    async def get(self, name_or_uuid: str):

        async with self._session.get(
            APPLICATIONS_BASE_PATH + "/{}".format(name_or_uuid)
        ) as resp:
            return await resp.text()

    @api_response(ApplicationResponse)
    async def list(self):

        async with self._session.get(APPLICATIONS_BASE_PATH) as resp:
            return await resp.text()

    async def delete(self, name_or_uuid: str):
        async with self._session.delete(
            APPLICATIONS_BASE_PATH + "/{}".format(name_or_uuid)
        ) as resp:
            return await resp.text()

    @api_response(ApplicationResponse)
    async def create(self, create_application_parameters: CreateApplicationParams):
        async with self._session.post(
            APPLICATIONS_BASE_PATH,
            data=json.dumps(
                create_application_parameters.repr_json(), cls=ComplexEncoder
            ),
        ) as resp:
            return await resp.text()
