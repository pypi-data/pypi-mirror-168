"""Classes related to card endpoints
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, ClassVar, Optional
from uuid import UUID

import packaging.version
from pydantic import BaseModel, PrivateAttr
from pydantic.fields import Field

from metabase_tools.common import log_call
from metabase_tools.exceptions import InvalidParameters
from metabase_tools.models.collection_model import CollectionItem
from metabase_tools.models.generic_model import Item, MissingParam
from metabase_tools.models.user_model import UserItem

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = logging.getLogger(__name__)


class CardItem(Item):
    """Card object class with related methods"""

    _BASE_EP: ClassVar[str] = "/card/{id}"

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)
    _server_version: Optional[packaging.version.Version] = PrivateAttr(None)

    description: Optional[str]
    archived: bool
    collection_position: Optional[int]
    table_id: Optional[int]
    result_metadata: Optional[list[dict[str, Any]]]
    creator: UserItem
    database_id: Optional[int]
    enable_embedding: bool
    collection_id: Optional[int]
    query_type: Optional[str]
    creator_id: int
    updated_at: datetime
    made_public_by_id: Optional[int]
    embedding_params: Optional[dict[str, Any]]
    cache_ttl: Optional[str]
    dataset_query: dict[str, Any]
    display: str
    last_edit_info: Optional[dict[str, Any]] = Field(alias="last-edit-info")
    visualization_settings: dict[str, Any]
    collection: Optional[CollectionItem]
    dataset: Optional[int]
    created_at: datetime
    public_uuid: Optional[UUID]
    can_write: Optional[bool]
    dashboard_count: Optional[int]
    is_favorite: Optional[bool] = Field(alias="favorite")

    average_query_time: Optional[int]
    collection_preview: Optional[bool]
    entity_id: Optional[str]
    last_query_start: Optional[datetime]
    moderation_reviews: Optional[list[Any]]
    parameter_mappings: Optional[list[Any]]
    parameters: Optional[list[Any]]

    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        super().set_adapter(adapter=adapter)

    def refresh(self: CardItem) -> CardItem:
        """Returns refreshed copy of the card

        Returns:
            CardItem: self
        """
        return super().refresh()

    @log_call
    def delete(self: CardItem) -> None:
        """DEPRECATED; use archive instead"""
        raise NotImplementedError

    def _make_update(self: CardItem, **kwargs: Any) -> CardItem:
        """Makes update request

        Args:
            self (CardItem)

        Returns:
            CardItem: self
        """
        return super()._make_update(**kwargs)

    @log_call
    def update(
        self: CardItem,
        visualization_settings: Optional[
            dict[str, str] | MissingParam
        ] = MissingParam(),
        description: Optional[str | MissingParam] = MissingParam(),
        archived: Optional[bool | MissingParam] = MissingParam(),
        collection_position: Optional[int | MissingParam] = MissingParam(),
        result_metadata: Optional[list[dict[str, str]] | MissingParam] = MissingParam(),
        metadata_checksum: Optional[str | MissingParam] = MissingParam(),
        enable_embedding: Optional[bool | MissingParam] = MissingParam(),
        collection_id: Optional[int | MissingParam] = MissingParam(),
        name: Optional[str | MissingParam] = MissingParam(),
        embedding_params: Optional[dict[str, str] | MissingParam] = MissingParam(),
        dataset_query: Optional[dict[str, Any] | MissingParam] = MissingParam(),
        display: Optional[str | MissingParam] = MissingParam(),
        **kwargs: Any,
    ) -> CardItem:
        """Updates a card using the provided parameters

        Args:
            self (CardItem)
            visualization_settings (dict[str, str], optional)
            description (str, optional)
            archived (bool, optional)
            collection_position (int, optional)
            result_metadata (list[dict[str, str]], optional)
            metadata_checksum (str, optional)
            enable_embedding (bool, optional)
            collection_id (int, optional)
            name (str, optional)
            embedding_params (dict[str, str], optional)
            dataset_query (dict[str, Any], optional)
            display (str, optional)

        Returns:
            CardItem: _description_
        """
        return self._make_update(
            visualization_settings=visualization_settings,
            description=description,
            archived=archived,
            collection_position=collection_position,
            result_metadata=result_metadata,
            metadata_checksum=metadata_checksum,
            enable_embedding=enable_embedding,
            collection_id=collection_id,
            name=name,
            embedding_params=embedding_params,
            dataset_query=dataset_query,
            display=display,
            **kwargs,
        )

    @log_call
    def archive(self: CardItem) -> CardItem:
        """Method for archiving a card

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            CardItem: Object of the relevant type
        """
        return super().archive()

    def unarchive(self: CardItem) -> CardItem:
        """Method for unarchiving a card

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            CardItem: Object of the relevant type
        """
        return super().unarchive()

    @log_call
    def related(self: CardItem) -> CardRelatedObjects:
        """Objects related to target

        Returns:
            CardRelatedObjects
        """
        if self._adapter:
            result = self._adapter.get(endpoint=f"/card/{self.id}/related")
            if isinstance(result, dict):
                result["card_id"] = self.id
                return CardRelatedObjects(**result)
        raise InvalidParameters

    @log_call
    def favorite(self: CardItem) -> CardItem:
        """Mark card as favorite

        Returns:
            dict: Result of favoriting operation
        """
        if self._server_version and self._server_version >= packaging.version.Version(
            "v0.40"
        ):
            raise NotImplementedError("This function was deprecated in Metabase v0.40")
        if self._adapter:
            result = self._adapter.post(endpoint=f"/card/{self.id}/favorite")
            if isinstance(result, dict):
                return self.refresh()
        raise InvalidParameters

    @log_call
    def unfavorite(self: CardItem) -> CardItem:
        """Unfavorite card

        Returns:
            dict: Result of unfavoriting operation
        """
        if self._server_version and self._server_version >= packaging.version.Version(
            "v0.40"
        ):
            raise NotImplementedError("This function was deprecated in Metabase v0.40")
        if self._adapter:
            result = self._adapter.delete(endpoint=f"/card/{self.id}/favorite")
            if isinstance(result, dict):
                return self.refresh()
        raise InvalidParameters

    @log_call
    def share(self: CardItem) -> CardItem:
        """Generate publicly-accessible link for card

        Returns:
            dict: UUID to be used in public link.
        """
        if self._adapter:
            result = self._adapter.post(endpoint=f"/card/{self.id}/public_link")
            if isinstance(result, dict) and "uuid" in result:
                return self.refresh()
        raise InvalidParameters

    @log_call
    def unshare(self: CardItem) -> CardItem:
        """Remove publicly-accessible links for card

        Returns:
            dict: UUID to be used in public link.
        """
        if self._adapter:
            result = self._adapter.delete(endpoint=f"/card/{self.id}/public_link")
            if isinstance(result, dict) and isinstance(self.id, int):
                card = self._adapter.cards.get([self.id])[0]
                return card
        raise InvalidParameters

    @log_call
    def query(self: CardItem) -> CardQueryResult:
        """Execute a query stored in card(s)

        Returns:
            CardQueryResult: Results of query
        """
        if self._adapter:
            result = self._adapter.post(endpoint=f"/card/{self.id}/query")
            if isinstance(result, dict):
                return CardQueryResult(**result)
        raise InvalidParameters


class CardQueryResult(BaseModel):
    """Object for results of a card query"""

    data: dict[str, Any]
    database_id: int
    started_at: datetime
    json_query: dict[str, Any]
    average_execution_time: Optional[int]
    status: str
    context: str
    row_count: int
    running_time: int


class CardRelatedObjects(BaseModel):
    """Objects related to the specified card"""

    card_id: int
    table: Optional[str]
    metrics: list[dict[str, int]]
    segments: list[dict[str, int]]
    dashboard_mates: list[dict[str, int]] = Field(alias="dashboard-mates")
    similar_questions: list[dict[str, int]] = Field(alias="similar-questions")
    canonical_metric: Optional[str] = Field(alias="canonical-metric")
    dashboards: list[dict[str, int]]
    collections: list[dict[str, int]]
