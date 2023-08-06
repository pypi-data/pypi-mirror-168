""" Register User Command Definition """

from starlette import status

from ..contracts.dto.request_status_codes import RequestStatusCodes
from ..contracts.dto.user.base import UserBase
from ..contracts.dto.wrapped_request import WrappedRequest
from ..contracts.request_verb import RequestVerb
from ..contracts.requests.register_user_request import RegisterUserRequest
from .abstract_command import AbstractCommand


class RegisterUserCommand(AbstractCommand):
    """
    Register User Command

    Methods
    -------
    execute(self, request: User) -> None
        Register User
    """

    def execute(self, request: RegisterUserRequest) -> UserBase:
        """
        Register User

        Parameters
        ----------
        request: RegisterUserRequest
        """

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.POST,
            url=f"https://{self.options.tld}/auth/v1/register",
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[], retry=[]),
            data=request.dict(by_alias=True),
        )
        response: dict = self.wrapped_request(request=request)
        return UserBase.parse_obj(response)
