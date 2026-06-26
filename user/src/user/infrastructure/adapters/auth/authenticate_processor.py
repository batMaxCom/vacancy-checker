from httpx import AsyncClient, HTTPStatusError, RequestError
from starlette.datastructures import Headers
from starlette.requests import Request
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from user.application.common.application_error import ApplicationError, ApplicationTypeError
from user.application.common.const.errors import (
    AUTH_SERVICE_UNAVAILABLE,
    INVALID_TOKEN,
    UNAUTHENTICATED,
)
from user.application.ports import Logger
from user.application.ports.auth import AuthenticateProcessor
from user.entrypoint.web.config import AuthConfig


class AuthenticateProcessorImpl(AuthenticateProcessor):
    def __init__(
        self,
        request: Request,
        client: AsyncClient,
        auth_config: AuthConfig,
        logger: Logger,
    ) -> None:
        self.__request = request
        self.__client = client
        self.__logger = logger
        self.__auth_config = auth_config

    async def process(self) -> None:
        if not (access_token := self.__request.headers.get("X-Access-Token")):
            raise ApplicationError(
                type=ApplicationTypeError.UNAUTHORIZED,
                message=UNAUTHENTICATED,
            )
        try:
            response = await self.__client.get(
                url=self.__auth_config.authenticate_url,
                headers={
                    "X-Access-Token": access_token
                }
            )
            response.raise_for_status()
            response_json = response.json().get("result")

        except RequestError as error:
            message = f"Request failed: {error}"
            await self.__logger.aexception(
                event="authenticate",
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                message=message,
            )
            raise ApplicationError(
                type=ApplicationTypeError.UNAUTHORIZED,
                message=AUTH_SERVICE_UNAVAILABLE,
            ) from error

        except HTTPStatusError:
            raise ApplicationError(
                type=ApplicationTypeError.UNAUTHORIZED,
                message=INVALID_TOKEN,
            ) from None
        except Exception as e:
            print(e)
        else:
            if not response_json.get("expires_at"):
                raise ApplicationError(
                    type=ApplicationTypeError.UNAUTHORIZED,
                    message=UNAUTHENTICATED,
                )
            user_id = response_json.get("user_id")
            role = response_json.get("role")

            if user_id:
                self.__request.scope["headers"].append((b"x-user-id", user_id.encode()))

            if role :
                self.__request.scope["headers"].append((b"x-api-roles", role.encode()))

            self.__request._headers = Headers(scope=self.__request.scope)
