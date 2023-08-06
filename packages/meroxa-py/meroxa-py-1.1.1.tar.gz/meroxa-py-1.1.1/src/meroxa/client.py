import aiohttp

from .applications import Applications
from .connectors import Connectors
from .constants import MEROXA_API_ROUTE
from .constants import MEROXA_TIMEOUT
from .functions import Functions
from .pipelines import Pipelines
from .resources import Resources
from .users import Users


class Meroxa:
    """Asynchronous Meroxa API handler"""

    def __init__(
        self, auth, api_route=MEROXA_API_ROUTE, timeout=MEROXA_TIMEOUT, session=None
    ):
        """Create a session if one is not provided."""

        if api_route is None:
            api_route = MEROXA_API_ROUTE
        if session is None:
            session = aiohttp.ClientSession(
                base_url=api_route,
                headers={"Authorization": "Bearer {}".format(auth)},
                timeout=aiohttp.ClientTimeout(timeout),
            )

        self._session = session

        # Meroxa API Handlers
        self.applications = Applications(self._session)
        self.connectors = Connectors(self._session)
        self.functions = Functions(self._session)
        self.pipelines = Pipelines(self._session)
        self.resources = Resources(self._session)
        self.users = Users(self._session)

    """
    Enable async context management.

    e.g.:

    mySession = aiohttp.ClientSession()
    async with meroxa.Meroxa(session) as m:
        m.doTheThing()
    """

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        await self._session.close()
