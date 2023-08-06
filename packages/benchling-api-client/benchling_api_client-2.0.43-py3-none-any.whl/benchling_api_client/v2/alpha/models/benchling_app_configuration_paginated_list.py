from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_config_item import AppConfigItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="BenchlingAppConfigurationPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class BenchlingAppConfigurationPaginatedList:
    """  """

    _app_configuration_items: Union[Unset, List[AppConfigItem]] = UNSET
    _next_token: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("app_configuration_items={}".format(repr(self._app_configuration_items)))
        fields.append("next_token={}".format(repr(self._next_token)))
        return "BenchlingAppConfigurationPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_configuration_items: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._app_configuration_items, Unset):
            app_configuration_items = []
            for app_configuration_items_item_data in self._app_configuration_items:
                app_configuration_items_item = app_configuration_items_item_data.to_dict()

                app_configuration_items.append(app_configuration_items_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app_configuration_items is not UNSET:
            field_dict["appConfigurationItems"] = app_configuration_items
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def get_app_configuration_items() -> Union[Unset, List[AppConfigItem]]:
            app_configuration_items = []
            _app_configuration_items = d.pop("appConfigurationItems")
            for app_configuration_items_item_data in _app_configuration_items or []:
                app_configuration_items_item = AppConfigItem.from_dict(app_configuration_items_item_data)

                app_configuration_items.append(app_configuration_items_item)

            return app_configuration_items

        app_configuration_items = (
            get_app_configuration_items()
            if "appConfigurationItems" in d
            else cast(Union[Unset, List[AppConfigItem]], UNSET)
        )

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        next_token = get_next_token() if "nextToken" in d else cast(Union[Unset, str], UNSET)

        benchling_app_configuration_paginated_list = cls(
            app_configuration_items=app_configuration_items,
            next_token=next_token,
        )

        return benchling_app_configuration_paginated_list

    @property
    def app_configuration_items(self) -> List[AppConfigItem]:
        if isinstance(self._app_configuration_items, Unset):
            raise NotPresentError(self, "app_configuration_items")
        return self._app_configuration_items

    @app_configuration_items.setter
    def app_configuration_items(self, value: List[AppConfigItem]) -> None:
        self._app_configuration_items = value

    @app_configuration_items.deleter
    def app_configuration_items(self) -> None:
        self._app_configuration_items = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
