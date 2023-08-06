from .types import MeroxaApiResponse
from .utils import api_response


class UserResponse(MeroxaApiResponse):
    def __init__(
        self,
        uuid: str,
        email: str,
        given_name: str,
        family_name: str,
        email_verified: bool,
        picture: str,
        last_login: str,
        features: list[str],
        username=None,
    ) -> None:
        self.uuid = uuid
        self.email = email
        self.given_name = given_name
        self.family_name = family_name
        self.email_verified = email_verified
        self.picture = picture
        self.last_login = last_login
        self.features = features
        self.username = username
        super().__init__()


class Users:
    def __init__(self, session) -> None:
        self._session = session

    @api_response(UserResponse)
    async def me(self):
        async with self._session.get("/v1/users/me") as resp:
            return await resp.text()
