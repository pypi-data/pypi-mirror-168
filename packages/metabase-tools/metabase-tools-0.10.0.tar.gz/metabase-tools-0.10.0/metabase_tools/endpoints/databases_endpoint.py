"""Classes related to database endpoints
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar, Optional

from metabase_tools.common import log_call
from metabase_tools.endpoints.generic_endpoint import Endpoint
from metabase_tools.models.database_model import DatabaseItem
from metabase_tools.models.generic_model import MissingParam

logger = logging.getLogger(__name__)


class Databases(Endpoint[DatabaseItem]):
    """Database related endpoint methods"""

    _BASE_EP: ClassVar[str] = "/database"
    _STD_OBJ: ClassVar[type] = DatabaseItem
    _required_params: ClassVar[list[str]] = ["name", "engine", "details"]

    @log_call
    def get(self, targets: Optional[list[int]] = None) -> list[DatabaseItem]:
        """Fetch list of databases

        Args:
            targets (list[int], optional): If provided, the list of databases to fetch

        Returns:
            list[DatabaseItem]
        """
        return super().get(targets=targets)

    def _make_create(self, **kwargs: Any) -> DatabaseItem:
        """Makes create request

        Args:
            self (DatabaseItem)

        Returns:
            DatabaseItem: self
        """
        return super()._make_create(**kwargs)

    @log_call
    def create(
        self,
        name: str | MissingParam = MissingParam(),
        engine: str | MissingParam = MissingParam(),
        details: dict[str, Any] | MissingParam = MissingParam(),
        is_full_sync: Optional[bool | MissingParam] = MissingParam(),
        is_on_demand: Optional[bool | MissingParam] = MissingParam(),
        schedules: Optional[dict[str, Any] | MissingParam] = MissingParam(),
        auto_run_queries: Optional[bool | MissingParam] = MissingParam(),
        **kwargs: Any,
    ) -> DatabaseItem:
        """Create a new database

        Args:
            name (str, optional)
            engine (str, optional)
            details (dict[str, Any], optional)
            is_full_sync (bool, optional)
            is_on_demand (bool, optional)
            schedules (dict[str, Any], optional)
            auto_run_queries (bool, optional)

        Returns:
            DatabaseItem
        """
        return super()._make_create(
            name=name,
            engine=engine,
            details=details,
            is_full_sync=is_full_sync,
            is_on_demand=is_on_demand,
            schedules=schedules,
            auto_run_queries=auto_run_queries,
            **kwargs,
        )

    @log_call
    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[DatabaseItem]] = None,
    ) -> list[DatabaseItem]:
        """Method to search a list of databases meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[DatabaseItem], optional): Provide to search an existing \
                list, by default pulls from API

        Returns:
            list[DatabaseItem]: List of databases of the relevant type
        """
        return super().search(search_params=search_params, search_list=search_list)
