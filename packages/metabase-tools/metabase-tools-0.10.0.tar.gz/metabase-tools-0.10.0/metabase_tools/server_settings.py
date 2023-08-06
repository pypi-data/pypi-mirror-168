"""Classes related to server settings for Metabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, Field, PrivateAttr

from metabase_tools.exceptions import MetabaseApiException

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi


def replace_hyphens(python_member_name: str) -> str:
    """Used as an alias generator to convert Metabase settings names to Python-friendl\
        y names

    Args:
        python_member_name (str): Python friendly name

    Returns:
        str: Metabase setting name
    """
    return python_member_name.replace("_", "-")


class Setting(BaseModel):
    """Individual setting on the server"""

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)

    key: str
    value: Optional[Any]
    is_env_setting: bool
    env_name: str
    description: str
    default: Optional[Any]

    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        self._adapter = adapter

    def update(self, new_value: Any) -> dict[str, Any]:
        """Updates the setting to the provided value after testing basic compatibility

        Args:
            new_value (Any): Desired value for the setting

        Raises:
            TypeError: new_value was not the same type as current value
            MetabaseApiException

        Returns:
            dict[str, Any]: Status of setting change
        """
        if not self._value_type_compatible(new_value):
            raise TypeError
        if self._adapter:
            result = self._adapter.put(
                endpoint=f"/setting/{self.key}", json={"value": new_value}
            )
            if isinstance(result, dict):
                new_def = {
                    setting["key"]: setting
                    for setting in self._adapter.get(endpoint="/setting")
                    if isinstance(setting, dict)
                }[self.key]
                if isinstance(new_def, dict):
                    self.value = new_def["value"]
                return result
        raise MetabaseApiException

    def _value_type_compatible(self, new_value: Any) -> bool:
        if self.value is None or new_value is None:
            return True
        if isinstance(new_value, type(self.value)):
            return True
        return False


class ServerSettings(BaseModel, alias_generator=replace_hyphens, extra="ignore"):
    """Settings for a Metabase server"""

    _adapter: MetabaseApi = PrivateAttr(None)

    admin_email: Setting
    anon_tracking_enabled: Setting
    application_colors: Setting
    application_favicon_url: Setting
    application_logo_url: Setting
    application_name: Setting
    available_locales: Setting
    available_timezones: Setting
    breakout_bin_width: Setting
    breakout_bins_num: Setting
    check_for_updates: Setting
    custom_formatting: Setting
    custom_geojson: Setting
    email_configured: Setting = Field(..., alias="email-configured?")
    email_from_address: Setting
    email_smtp_host: Setting
    email_smtp_password: Setting
    email_smtp_port: Setting
    email_smtp_security: Setting
    email_smtp_username: Setting
    embedding_app_origin: Setting
    embedding_secret_key: Setting
    enable_audit_app: Setting = Field(..., alias="enable-audit-app?")
    enable_embedding: Setting
    enable_enhancements: Setting = Field(..., alias="enable-enhancements?")
    enable_nested_queries: Setting
    enable_password_login: Setting
    enable_public_sharing: Setting
    enable_query_caching: Setting
    enable_sandboxes: Setting = Field(..., alias="enable-sandboxes?")
    enable_sso: Setting = Field(..., alias="enable-sso?")
    enable_whitelabeling: Setting = Field(..., alias="enable-whitelabeling?")
    enable_xrays: Setting
    engines: Setting
    field_filter_operators_enabled: Optional[Setting] = Field(
        alias="field-filter-operators-enabled?"
    )
    ga_code: Setting
    google_auth_auto_create_accounts_domain: Setting
    google_auth_client_id: Setting
    has_sample_dataset: Optional[Setting] = Field(alias="has-sample-dataset?")
    hide_embed_branding: Setting = Field(..., alias="hide-embed-branding?")
    humanization_strategy: Setting
    landing_page: Setting
    ldap_attribute_email: Setting
    ldap_attribute_firstname: Setting
    ldap_attribute_lastname: Setting
    ldap_bind_dn: Setting
    ldap_configured: Setting = Field(..., alias="ldap-configured?")
    ldap_enabled: Setting
    ldap_group_base: Setting
    ldap_group_mappings: Setting
    ldap_group_sync: Setting
    ldap_host: Setting
    ldap_password: Setting
    ldap_port: Setting
    ldap_security: Setting
    ldap_user_base: Setting
    ldap_user_filter: Setting
    map_tile_server_url: Setting
    metabot_enabled: Optional[Setting]
    password_complexity: Setting
    premium_embedding_token: Setting
    premium_features: Optional[Setting]
    query_caching_max_kb: Setting
    query_caching_max_ttl: Setting
    query_caching_min_ttl: Setting
    query_caching_ttl_ratio: Setting
    redirect_all_requests_to_https: Setting
    redshift_fetch_size: Optional[Setting]
    report_timezone: Setting
    report_timezone_short: Setting
    search_typeahead_enabled: Setting
    setup_token: Setting
    show_homepage_data: Setting
    show_homepage_xrays: Setting
    site_locale: Setting
    site_name: Setting
    site_url: Setting
    slack_token: Setting
    source_address_header: Setting
    ssh_heartbeat_interval_sec: Setting
    ssl_certificate_public_key: Setting
    start_of_week: Setting
    version: Setting
    version_info: Setting
    version_info_last_checked: Setting

    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        self._adapter = adapter

        for setting in self.__dict__.values():
            if isinstance(setting, Setting):
                setting.set_adapter(adapter)
