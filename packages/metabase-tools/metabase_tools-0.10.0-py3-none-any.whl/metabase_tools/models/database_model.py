"""Classes related to database endpoints
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from pydantic import Field, PrivateAttr

from metabase_tools.common import log_call
from metabase_tools.models.generic_model import Item, MissingParam

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = logging.getLogger(__name__)


class DatabaseItem(Item):
    """Database object class with related methods"""

    _BASE_EP: ClassVar[str] = "/database/{id}"

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)

    description: Optional[str]
    features: list[str]
    cache_field_values_schedule: str
    timezone: Optional[str]
    auto_run_queries: bool
    metadata_sync_schedule: str
    caveats: Optional[str]
    is_full_sync: bool
    updated_at: datetime
    native_permissions: Optional[str]
    details: dict[str, Any]
    is_sample: bool
    is_on_demand: bool
    options: Optional[str]
    engine: str
    refingerprint: Optional[str]
    created_at: datetime
    points_of_interest: Optional[str]
    schedules: Optional[dict[str, Any]]
    cache_ttl: Optional[int]
    creator_id: Optional[int]
    initial_sync_status: Optional[str]
    settings: Optional[Any]
    can_manage: Optional[bool] = Field(alias="can-manage")

    def refresh(self: DatabaseItem) -> DatabaseItem:
        """Returns refreshed copy of the database

        Returns:
            DatabaseItem: self
        """
        return super().refresh()

    @log_call
    def delete(self: DatabaseItem) -> None:
        """Deletes the database"""
        return super().delete()

    def _make_update(self: DatabaseItem, **kwargs: Any) -> DatabaseItem:
        """Makes update request

        Args:
            self (DatabaseItem)

        Returns:
            DatabaseItem: self
        """
        return super()._make_update(**kwargs)

    @log_call
    def update(
        self: DatabaseItem,
        engine: Optional[str | MissingParam] = MissingParam(),
        schedules: Optional[dict[str, Any] | MissingParam] = MissingParam(),
        refingerprint: Optional[bool | MissingParam] = MissingParam(),
        points_of_interest: Optional[str | MissingParam] = MissingParam(),
        description: Optional[str | MissingParam] = MissingParam(),
        name: Optional[str | MissingParam] = MissingParam(),
        caveats: Optional[str | MissingParam] = MissingParam(),
        cache_ttl: Optional[int | MissingParam] = MissingParam(),
        details: Optional[dict[str, Any] | MissingParam] = MissingParam(),
        **kwargs: Any,
    ) -> DatabaseItem:
        """Updates a database using the provided parameters

        Args:
            self (DatabaseItem)
            engine (str, optional)
            schedules (dict[str, Any], optional)
            refingerprint (bool, optional)
            points_of_interest (str, optional)
            description (str, optional)
            name (str, optional)
            caveats (str, optional)
            cache_ttl (int, optional)
            details (dict[str, Any], optional)

        Returns:
            DatabaseItem
        """
        return self._make_update(
            engine=engine,
            schedules=schedules,
            refingerprint=refingerprint,
            points_of_interest=points_of_interest,
            description=description,
            name=name,
            caveats=caveats,
            cache_ttl=cache_ttl,
            details=details,
            **kwargs,
        )
