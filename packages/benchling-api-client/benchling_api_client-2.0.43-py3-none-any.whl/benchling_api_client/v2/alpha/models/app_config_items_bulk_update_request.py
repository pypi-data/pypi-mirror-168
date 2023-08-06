from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.app_config_item_bulk_update import AppConfigItemBulkUpdate
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppConfigItemsBulkUpdateRequest")


@attr.s(auto_attribs=True, repr=False)
class AppConfigItemsBulkUpdateRequest:
    """  """

    _app_configuration_items: List[AppConfigItemBulkUpdate]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("app_configuration_items={}".format(repr(self._app_configuration_items)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppConfigItemsBulkUpdateRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_configuration_items = []
        for app_configuration_items_item_data in self._app_configuration_items:
            app_configuration_items_item = app_configuration_items_item_data.to_dict()

            app_configuration_items.append(app_configuration_items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app_configuration_items is not UNSET:
            field_dict["appConfigurationItems"] = app_configuration_items

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def get_app_configuration_items() -> List[AppConfigItemBulkUpdate]:
            app_configuration_items = []
            _app_configuration_items = d.pop("appConfigurationItems")
            for app_configuration_items_item_data in _app_configuration_items:
                app_configuration_items_item = AppConfigItemBulkUpdate.from_dict(
                    app_configuration_items_item_data
                )

                app_configuration_items.append(app_configuration_items_item)

            return app_configuration_items

        app_configuration_items = (
            get_app_configuration_items()
            if "appConfigurationItems" in d
            else cast(List[AppConfigItemBulkUpdate], UNSET)
        )

        app_config_items_bulk_update_request = cls(
            app_configuration_items=app_configuration_items,
        )

        app_config_items_bulk_update_request.additional_properties = d
        return app_config_items_bulk_update_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def app_configuration_items(self) -> List[AppConfigItemBulkUpdate]:
        if isinstance(self._app_configuration_items, Unset):
            raise NotPresentError(self, "app_configuration_items")
        return self._app_configuration_items

    @app_configuration_items.setter
    def app_configuration_items(self, value: List[AppConfigItemBulkUpdate]) -> None:
        self._app_configuration_items = value
