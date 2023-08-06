"""Classes related to card endpoints
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar, Optional

from metabase_tools.common import log_call
from metabase_tools.endpoints.generic_endpoint import Endpoint
from metabase_tools.models.card_model import CardItem
from metabase_tools.models.generic_model import MissingParam

logger = logging.getLogger(__name__)


class Cards(Endpoint[CardItem]):
    """Card related endpoint methods"""

    _BASE_EP: ClassVar[str] = "/card"
    _STD_OBJ: ClassVar[type] = CardItem

    _required_params: ClassVar[list[str]] = [
        "visualization_settings",
        "name",
        "dataset_query",
        "display",
    ]

    @log_call
    def get(self, targets: Optional[list[int]] = None) -> list[CardItem]:
        """Fetch list of cards

        Args:
            targets (list[int], optional): If provided, the list of cards to fetch

        Returns:
            list[CardItem]
        """
        return super().get(targets=targets)

    def _make_create(self, **kwargs: Any) -> CardItem:
        """Makes create request

        Args:
            self (CardItem)

        Returns:
            CardItem: self
        """
        return super()._make_create(**kwargs)

    @log_call
    def create(
        self,
        visualization_settings: dict[str, Any] | MissingParam = MissingParam(),
        name: str | MissingParam = MissingParam(),
        dataset_query: dict[str, Any] | MissingParam = MissingParam(),
        display: str | MissingParam = MissingParam(),
        description: Optional[str | MissingParam] = MissingParam(),
        collection_position: Optional[int | MissingParam] = MissingParam(),
        result_metadata: Optional[list[dict[str, Any]] | MissingParam] = MissingParam(),
        metadata_checksum: Optional[str | MissingParam] = MissingParam(),
        collection_id: Optional[int | MissingParam] = MissingParam(),
        **kwargs: Any,
    ) -> CardItem:
        """Creates a new card

        Args:
            visualization_settings (dict[str, Any])
            name (str)
            dataset_query (dict[str, Any])
            display (str)
            description (str, optional)
            collection_position (int, optional)
            result_metadata (list[dict[str, Any]], optional)
            metadata_checksum (str, optional)
            collection_id (int, optional)

        Returns:
            CardItem
        """
        return self._make_create(
            visualization_settings=visualization_settings,
            description=description,
            collection_position=collection_position,
            result_metadata=result_metadata,
            metadata_checksum=metadata_checksum,
            collection_id=collection_id,
            name=name,
            dataset_query=dataset_query,
            display=display,
            **kwargs,
        )

    @log_call
    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[CardItem]] = None,
    ) -> list[CardItem]:
        """Method to search a list of cards meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[CardItem], optional): Provide to search an existing \
                list, by default pulls from API

        Returns:
            list[CardItem]: List of cards of the relevant type
        """
        return super().search(search_params=search_params, search_list=search_list)

    @log_call
    def embeddable(self) -> list[CardItem]:
        """Fetch list of cards with embedding enabled

        Raises:
            EmptyDataReceived: If no cards have embedding enabled

        Returns:
            list[CardItem]: List of cards with embedding enabled
        """
        cards = self._adapter.get(endpoint="/card/embeddable")
        card_ids = [card["id"] for card in cards if isinstance(card, dict)]
        result = self._adapter.cards.get(card_ids)
        return result
