"""Classes related to collection endpoints
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar, Optional

from metabase_tools.common import log_call
from metabase_tools.endpoints.generic_endpoint import Endpoint
from metabase_tools.exceptions import EmptyDataReceived
from metabase_tools.models.collection_model import CollectionItem
from metabase_tools.models.generic_model import MissingParam

logger = logging.getLogger(__name__)


class Collections(Endpoint[CollectionItem]):
    """Card related endpoint methods"""

    _BASE_EP: ClassVar[str] = "/collection"
    _STD_OBJ: ClassVar[type] = CollectionItem
    _required_params: ClassVar[list[str]] = ["name", "color"]

    @log_call
    def get(self, targets: Optional[list[int]] = None) -> list[CollectionItem]:
        """Fetch list of collections

        Args:
            targets (list[int], optional): If provided, the list of collections to fetch

        Returns:
            list[CollectionItem]
        """
        return super().get(targets=targets)

    def _make_create(self, **kwargs: Any) -> CollectionItem:
        """Makes create request

        Args:
            self (CollectionItem)

        Returns:
            CollectionItem: self
        """
        return super()._make_create(**kwargs)

    @log_call
    def create(
        self,
        name: str | MissingParam = MissingParam(),
        color: str | MissingParam = MissingParam(),
        description: Optional[str | MissingParam] = MissingParam(),
        parent_id: Optional[int | MissingParam] = MissingParam(),
        namespace: Optional[str | MissingParam] = MissingParam(),
        **kwargs: Any,
    ) -> CollectionItem:
        """Creates a new collection

        Args:
            name (str, optional)
            color (str, optional)
            description (str, optional)
            parent_id (int, optional)
            namespace (str, optional)

        Returns:
            CollectionItem
        """
        return self._make_create(
            name=name,
            color=color,
            description=description,
            parent_id=parent_id,
            namespace=namespace,
            **kwargs,
        )

    @log_call
    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[CollectionItem]] = None,
    ) -> list[CollectionItem]:
        """Method to search a list of cards meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[CollectionItem], optional): Provide to search an existing\
                 list, by default pulls from API

        Returns:
            list[CollectionItem]: List of cards of the relevant type
        """
        return super().search(search_params=search_params, search_list=search_list)

    @log_call
    def get_tree(self) -> list[dict[str, Any]]:
        """Collection tree

        Args:
            adapter (MetabaseApi): Connection to Metabase API

        Raises:
            EmptyDataReceived: No data returned from API

        Returns:
            list[dict]: Representation of collection tree
        """
        response = self._adapter.get(endpoint="/collection/tree")
        if isinstance(response, list) and all(
            isinstance(record, dict) for record in response
        ):
            return response
        raise EmptyDataReceived

    @staticmethod
    def _flatten_tree(parent: dict[str, Any], path: str = "/") -> list[dict[str, Any]]:
        """Recursive function to flatten collection tree to show the full path for all\
             collections

        Args:
            parent (dict): Parent collection
            path (str, optional): Path to parent collection. Defaults to "/".

        Returns:
            list[dict]: Flattened list
        """
        children = []
        for child in parent["children"]:
            children.append(
                {
                    "id": child["id"],
                    "name": child["name"],
                    "path": f'{path}/{parent["name"]}/{child["name"]}'.replace(
                        "//", "/"
                    ),
                }
            )
            if "children" in child and len(child["children"]) > 0:
                grandchildren = Collections._flatten_tree(
                    child, f'{path}/{parent["name"]}'.replace("//", "/")
                )
                if isinstance(grandchildren, list):
                    children.extend(grandchildren)
                else:
                    children.append(grandchildren)
        return children

    @log_call
    def get_flat_list(self) -> list[dict[str, Any]]:
        """Flattens collection tree so the full path of each collection is shown

        Args:
            adapter (MetabaseApi): Connection to Metabase API

        Returns:
            list[dict]: Flattened collection tree
        """
        tree = self.get_tree()
        folders = []
        for root_folder in tree:
            if root_folder["personal_owner_id"] is not None:  # Skips personal folders
                continue
            folders.append(
                {
                    "id": root_folder["id"],
                    "name": root_folder["name"],
                    "path": f'/{root_folder["name"]}',
                }
            )
            folders.extend(Collections._flatten_tree(root_folder))
        return folders

    @log_call
    def graph(self) -> dict[str, Any]:
        """Graph of collection permissions

        Returns:
            dict: graph of collection
        """
        if self._adapter:
            result = self._adapter.get(endpoint="/collection/graph")
            if isinstance(result, dict):
                return result
        raise EmptyDataReceived
