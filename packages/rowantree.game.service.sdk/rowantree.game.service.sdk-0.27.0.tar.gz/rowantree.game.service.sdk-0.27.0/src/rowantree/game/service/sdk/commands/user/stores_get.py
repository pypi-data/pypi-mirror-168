""" User Stores Get Command Definition """
from typing import Optional

from starlette import status

from rowantree.contracts import StoreType, UserStore

from ...contracts.dto.request_status_codes import RequestStatusCodes
from ...contracts.dto.wrapped_request import WrappedRequest
from ...contracts.request_verb import RequestVerb
from ...contracts.responses.stores_get import StoresGetResponse
from ..abstract_command import AbstractCommand


class UserStoresGetCommand(AbstractCommand):
    """
    User Stores Get Command
    Gets the (unique) list of user stores.

    Methods
    -------
    execute(self, user_guid: str) -> dict[StoreType, UserStore]
        Executes the command.
    """

    def execute(self, user_guid: Optional[str] = None) -> dict[StoreType, UserStore]:
        """
        Gets the (unique) list of user stores.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_stores: dict[StoreType, UserStore]
        """

        target_guid: str = self.demand_user_guid(user_guid=user_guid)

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.GET,
            url=f"https://api.{self.options.tld}/game/v1/user/{target_guid}/stores",
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[status.HTTP_401_UNAUTHORIZED], retry=[]),
        )
        response: dict = self.wrapped_request(request=request)
        stores_get_response: StoresGetResponse = StoresGetResponse.parse_obj(response)
        return stores_get_response.stores
