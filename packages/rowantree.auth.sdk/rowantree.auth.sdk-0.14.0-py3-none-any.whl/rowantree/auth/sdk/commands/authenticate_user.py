""" Action Queue Process Command Definition """

from starlette import status

from ..contracts.dto.request_status_codes import RequestStatusCodes
from ..contracts.dto.token import Token
from ..contracts.dto.wrapped_request import WrappedRequest
from ..contracts.request_verb import RequestVerb
from ..contracts.requests.authenticate_user_request import AuthenticateUserRequest
from .abstract_command import AbstractCommand


class AuthenticateUserCommand(AbstractCommand):
    """
    Authenticate User Command

    Methods
    -------
    execute(self, request: AuthenticateUserRequest) -> None
        Executes the command.
    """

    def execute(self, request: AuthenticateUserRequest) -> Token:
        """
        Executes the command.

        Parameters
        ----------
        request: AuthenticateUserRequest
        """

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.POST,
            url=f"https://{self.options.tld}/auth/v1/token",
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[status.HTTP_401_UNAUTHORIZED], retry=[]),
            data=request.dict(by_alias=True),
        )
        response: dict = self.wrapped_request(request=request)
        return Token.parse_obj(response)
