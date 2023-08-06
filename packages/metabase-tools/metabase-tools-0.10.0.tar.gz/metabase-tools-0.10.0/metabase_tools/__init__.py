"""Unofficial API wrapper for Metabase
"""

__version__ = "0.10.0"

from metabase_tools.exceptions import (
    AuthenticationFailure,
    EmptyDataReceived,
    InvalidDataReceived,
    InvalidParameters,
    ItemInPersonalCollection,
    ItemNotFound,
    MetabaseApiException,
    NoUpdateProvided,
    RequestFailure,
)
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.card_model import CardItem, CardQueryResult
from metabase_tools.models.collection_model import CollectionItem
from metabase_tools.models.database_model import DatabaseItem
from metabase_tools.models.user_model import UserItem
from metabase_tools.server_settings import ServerSettings, Setting
from metabase_tools.tools import MetabaseTools

__all__ = (
    "AuthenticationFailure",
    "EmptyDataReceived",
    "InvalidDataReceived",
    "InvalidParameters",
    "ItemNotFound",
    "ItemInPersonalCollection",
    "MetabaseApiException",
    "NoUpdateProvided",
    "RequestFailure",
    "MetabaseApi",
    "CardItem",
    "CardQueryResult",
    "CollectionItem",
    "DatabaseItem",
    "UserItem",
    "MetabaseTools",
    "ServerSettings",
    "Setting",
)
