"""
    Generic classes for Metabase
"""
from __future__ import annotations

import logging
from abc import ABC
from typing import TYPE_CHECKING, Any, ClassVar, Optional, TypeVar

import packaging.version
from pydantic import BaseModel, PrivateAttr

from metabase_tools.common import log_call
from metabase_tools.exceptions import InvalidParameters

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

T = TypeVar("T", bound="Item")
logger = logging.getLogger(__name__)


class MissingParam(BaseModel):
    """Used for parameters that were not supplied during an update or object creation"""


class Item(BaseModel, ABC, extra="forbid"):
    """Base class for all Metabase objects. Provides generic fields and methods."""

    _BASE_EP: ClassVar[str]

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)
    _server_version: Optional[packaging.version.Version] = PrivateAttr(None)

    id: int | str
    name: str

    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        self._adapter = adapter
        self._server_version = adapter.server_version

    def refresh(self: T) -> T:
        """Returns new copy of item from API

        Returns:
            T: self
        """
        if self._adapter:
            result = self._adapter.get(endpoint=self._BASE_EP.format(id=self.id))
            if isinstance(result, dict):
                obj = self.__class__(**result)
                obj.set_adapter(adapter=self._adapter)
                return obj
        return self

    def _make_update(self: T, **kwargs: Any) -> T:
        """Generic method for updating an object

        Args:
            payloads (dict): Details of update

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            T: Object of the relevant type
        """
        if self._adapter:
            # Eliminate parameters that were not provided
            changes = {
                k: v for k, v in kwargs.items() if not isinstance(v, MissingParam)
            }

            # Determine if there are any differences to update
            current_definition = self.dict()
            changes = {
                k: v
                for k, v in changes.items()
                if k in current_definition and v != current_definition[k]
            }

            if len(changes) == 0:
                return self

            result = self._adapter.put(
                endpoint=self._BASE_EP.format(id=self.id), json=changes
            )
            if isinstance(result, dict):
                obj = self.__class__(**result)
                obj.set_adapter(adapter=self._adapter)
                return obj
        raise InvalidParameters("Invalid target(s)")

    def archive(self: T) -> T:
        """Generic method for archiving an object

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            T: Object of the relevant type
        """
        payload = {"id": self.id, "archived": True}
        if self._adapter:
            result = self._adapter.put(
                endpoint=self._BASE_EP.format(id=self.id), json=payload
            )
            if isinstance(result, dict):
                obj = self.__class__(**result)
                obj.set_adapter(self._adapter)
                return obj
        raise InvalidParameters("Invalid target(s)")

    def unarchive(self: T) -> T:
        """Generic method for unarchiving an object

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            T: Object of the relevant type
        """
        payload = {"id": self.id, "archived": False}
        if self._adapter:
            result = self._adapter.put(
                endpoint=self._BASE_EP.format(id=self.id), json=payload
            )
            if isinstance(result, dict):
                obj = self.__class__(**result)
                obj.set_adapter(self._adapter)
                return obj
        raise InvalidParameters("Invalid target(s)")

    @log_call
    def delete(self) -> None:
        """Method to delete an object

        Raises:
            InvalidParameters: Invalid target
        """
        if self._adapter:
            _ = self._adapter.delete(endpoint=self._BASE_EP.format(id=self.id))
