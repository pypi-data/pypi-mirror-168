"""Classes related to card endpoints
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar, Optional

from metabase_tools.common import log_call
from metabase_tools.endpoints.generic_endpoint import Endpoint
from metabase_tools.exceptions import InvalidParameters
from metabase_tools.models.generic_model import MissingParam
from metabase_tools.models.user_model import UserItem

logger = logging.getLogger(__name__)


class Users(Endpoint[UserItem]):
    """Card related endpoint methods"""

    _BASE_EP: ClassVar[str] = "/user"
    _STD_OBJ: ClassVar[type] = UserItem
    _required_params: ClassVar[list[str]] = [
        "first_name",
        "last_name",
        "email",
        "password",
    ]

    @log_call
    def get(self, targets: Optional[list[int]] = None) -> list[UserItem]:
        """Fetch list of users

        Args:
            targets (list[int], optional): If provided, the list of users to fetch

        Returns:
            list[UserItem]
        """
        return super().get(targets=targets)

    def _make_create(self, **kwargs: Any) -> UserItem:
        """Makes create request

        Args:
            self (UserItem)

        Returns:
            UserItem: self
        """
        return super()._make_create(**kwargs)

    @log_call
    def create(
        self,
        first_name: str | MissingParam = MissingParam(),
        last_name: str | MissingParam = MissingParam(),
        email: str | MissingParam = MissingParam(),
        password: str | MissingParam = MissingParam(),
        group_ids: Optional[list[int] | MissingParam] = MissingParam(),
        login_attributes: Optional[str | MissingParam] = MissingParam(),
        **kwargs: Any,
    ) -> UserItem:
        """_summary_

        Args:
            first_name (str, optional)
            last_name (str, optional)
            email (str, optional)
            password (str, optional)
            group_ids (list[int], optional)
            login_attributes (str, optional)

        Returns:
            UserItem: _description_
        """
        return super()._make_create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            group_ids=group_ids,
            login_attributes=login_attributes,
            **kwargs,
        )

    @log_call
    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[UserItem]] = None,
    ) -> list[UserItem]:
        """Method to search a list of users meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[UserItem], optional): Provide to search an existing \
                list, by default pulls from API

        Returns:
            list[UserItem]: List of users of the relevant type
        """
        return super().search(search_params=search_params, search_list=search_list)

    @log_call
    def current(self) -> UserItem:
        """Current user details

        Raises:
            RequestFailure: Invalid response from API

        Returns:
            User: Current user details
        """
        response = self._adapter.get(endpoint="/user/current")
        if isinstance(response, dict):
            return UserItem(**response)
        raise InvalidParameters
