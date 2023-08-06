""" User State Get Command Definition """
from typing import Optional

from starlette import status

from rowantree.contracts import UserState

from ...contracts.dto.request_status_codes import RequestStatusCodes
from ...contracts.dto.wrapped_request import WrappedRequest
from ...contracts.request_verb import RequestVerb
from ..abstract_command import AbstractCommand


class UserStateGetCommand(AbstractCommand):
    """
    User State Get Command
    Gets the user game state.

    Methods
    -------
    execute(self, user_guid: str) -> UserState
        Executes the command.
    """

    def execute(self, user_guid: Optional[str] = None) -> UserState:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_state: UserState
            The user state object.
        """

        target_guid: str = self.demand_user_guid(user_guid=user_guid)

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.GET,
            url=f"https://api.{self.options.tld}/game/v1/user/{target_guid}/state",
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[status.HTTP_401_UNAUTHORIZED], retry=[]),
        )
        response: dict = self.wrapped_request(request=request)
        return UserState.parse_obj(response)
