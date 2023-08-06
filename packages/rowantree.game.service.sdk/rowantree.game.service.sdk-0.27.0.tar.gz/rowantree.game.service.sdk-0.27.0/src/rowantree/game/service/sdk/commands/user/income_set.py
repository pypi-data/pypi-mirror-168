""" User Income Set Command Definition """
from typing import Optional

from starlette import status

from ...contracts.dto.request_status_codes import RequestStatusCodes
from ...contracts.dto.wrapped_request import WrappedRequest
from ...contracts.request_verb import RequestVerb
from ...contracts.requests.user.income_set import UserIncomeSetRequest
from ..abstract_command import AbstractCommand


class UserIncomeSetCommand(AbstractCommand):
    """
    User Income Set Command
    Sets a user income. (Creates or dismisses a number of workers of the type).

    Methods
    -------
    execute(self, user_guid: str, request: UserIncomeSetRequest) -> None
        Executes the command.
    """

    def execute(self, request: UserIncomeSetRequest, user_guid: Optional[str] = None) -> None:
        """
        Executes the command.

        Parameters
        ----------
        user_guid
        request: UserIncomeSetRequest
            The UserIncomeSetRequest object for the update.
        """

        target_guid: str = self.demand_user_guid(user_guid=user_guid)

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.POST,
            url=f"https://api.{self.options.tld}/game/v1/user/{target_guid}/income",
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[status.HTTP_401_UNAUTHORIZED], retry=[]),
            data=request.dict(by_alias=True),
        )
        self.wrapped_request(request=request)
