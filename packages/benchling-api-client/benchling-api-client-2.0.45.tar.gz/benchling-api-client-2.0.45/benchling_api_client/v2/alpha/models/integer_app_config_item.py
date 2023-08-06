import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.app_config_item_api_mixin_app import AppConfigItemApiMixinApp
from ..models.archive_record import ArchiveRecord
from ..models.integer_app_config_item_type import IntegerAppConfigItemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegerAppConfigItem")


@attr.s(auto_attribs=True, repr=False)
class IntegerAppConfigItem:
    """  """

    _type: Union[Unset, IntegerAppConfigItemType] = UNSET
    _value: Union[Unset, None, int] = UNSET
    _description: Union[Unset, str] = UNSET
    _required_config: Union[Unset, bool] = UNSET
    _api_url: Union[Unset, str] = UNSET
    _app: Union[Unset, AppConfigItemApiMixinApp] = UNSET
    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _id: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _path: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("value={}".format(repr(self._value)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("required_config={}".format(repr(self._required_config)))
        fields.append("api_url={}".format(repr(self._api_url)))
        fields.append("app={}".format(repr(self._app)))
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("path={}".format(repr(self._path)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "IntegerAppConfigItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        value = self._value
        description = self._description
        required_config = self._required_config
        api_url = self._api_url
        app: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._app, Unset):
            app = self._app.to_dict()

        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        id = self._id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        path: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._path, Unset):
            path = self._path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type
        if value is not UNSET:
            field_dict["value"] = value
        if description is not UNSET:
            field_dict["description"] = description
        if required_config is not UNSET:
            field_dict["requiredConfig"] = required_config
        if api_url is not UNSET:
            field_dict["apiUrl"] = api_url
        if app is not UNSET:
            field_dict["app"] = app
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if id is not UNSET:
            field_dict["id"] = id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if path is not UNSET:
            field_dict["path"] = path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def get_type() -> Union[Unset, IntegerAppConfigItemType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = IntegerAppConfigItemType(_type)
                except ValueError:
                    type = IntegerAppConfigItemType.of_unknown(_type)

            return type

        type = get_type() if "type" in d else cast(Union[Unset, IntegerAppConfigItemType], UNSET)

        def get_value() -> Union[Unset, None, int]:
            value = d.pop("value")
            return value

        value = get_value() if "value" in d else cast(Union[Unset, None, int], UNSET)

        def get_description() -> Union[Unset, str]:
            description = d.pop("description")
            return description

        description = get_description() if "description" in d else cast(Union[Unset, str], UNSET)

        def get_required_config() -> Union[Unset, bool]:
            required_config = d.pop("requiredConfig")
            return required_config

        required_config = get_required_config() if "requiredConfig" in d else cast(Union[Unset, bool], UNSET)

        def get_api_url() -> Union[Unset, str]:
            api_url = d.pop("apiUrl")
            return api_url

        api_url = get_api_url() if "apiUrl" in d else cast(Union[Unset, str], UNSET)

        def get_app() -> Union[Unset, AppConfigItemApiMixinApp]:
            app: Union[Unset, AppConfigItemApiMixinApp] = UNSET
            _app = d.pop("app")
            if not isinstance(_app, Unset):
                app = AppConfigItemApiMixinApp.from_dict(_app)

            return app

        app = get_app() if "app" in d else cast(Union[Unset, AppConfigItemApiMixinApp], UNSET)

        def get_archive_record() -> Union[Unset, None, ArchiveRecord]:
            archive_record = None
            _archive_record = d.pop("archiveRecord")
            if _archive_record is not None and not isinstance(_archive_record, Unset):
                archive_record = ArchiveRecord.from_dict(_archive_record)

            return archive_record

        archive_record = (
            get_archive_record() if "archiveRecord" in d else cast(Union[Unset, None, ArchiveRecord], UNSET)
        )

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        id = get_id() if "id" in d else cast(Union[Unset, str], UNSET)

        def get_modified_at() -> Union[Unset, datetime.datetime]:
            modified_at: Union[Unset, datetime.datetime] = UNSET
            _modified_at = d.pop("modifiedAt")
            if _modified_at is not None and not isinstance(_modified_at, Unset):
                modified_at = isoparse(cast(str, _modified_at))

            return modified_at

        modified_at = get_modified_at() if "modifiedAt" in d else cast(Union[Unset, datetime.datetime], UNSET)

        def get_path() -> Union[Unset, List[str]]:
            path = cast(List[str], d.pop("path"))

            return path

        path = get_path() if "path" in d else cast(Union[Unset, List[str]], UNSET)

        integer_app_config_item = cls(
            type=type,
            value=value,
            description=description,
            required_config=required_config,
            api_url=api_url,
            app=app,
            archive_record=archive_record,
            id=id,
            modified_at=modified_at,
            path=path,
        )

        integer_app_config_item.additional_properties = d
        return integer_app_config_item

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
    def type(self) -> IntegerAppConfigItemType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: IntegerAppConfigItemType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def value(self) -> Optional[int]:
        if isinstance(self._value, Unset):
            raise NotPresentError(self, "value")
        return self._value

    @value.setter
    def value(self, value: Optional[int]) -> None:
        self._value = value

    @value.deleter
    def value(self) -> None:
        self._value = UNSET

    @property
    def description(self) -> str:
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET

    @property
    def required_config(self) -> bool:
        if isinstance(self._required_config, Unset):
            raise NotPresentError(self, "required_config")
        return self._required_config

    @required_config.setter
    def required_config(self, value: bool) -> None:
        self._required_config = value

    @required_config.deleter
    def required_config(self) -> None:
        self._required_config = UNSET

    @property
    def api_url(self) -> str:
        if isinstance(self._api_url, Unset):
            raise NotPresentError(self, "api_url")
        return self._api_url

    @api_url.setter
    def api_url(self, value: str) -> None:
        self._api_url = value

    @api_url.deleter
    def api_url(self) -> None:
        self._api_url = UNSET

    @property
    def app(self) -> AppConfigItemApiMixinApp:
        if isinstance(self._app, Unset):
            raise NotPresentError(self, "app")
        return self._app

    @app.setter
    def app(self, value: AppConfigItemApiMixinApp) -> None:
        self._app = value

    @app.deleter
    def app(self) -> None:
        self._app = UNSET

    @property
    def archive_record(self) -> Optional[ArchiveRecord]:
        if isinstance(self._archive_record, Unset):
            raise NotPresentError(self, "archive_record")
        return self._archive_record

    @archive_record.setter
    def archive_record(self, value: Optional[ArchiveRecord]) -> None:
        self._archive_record = value

    @archive_record.deleter
    def archive_record(self) -> None:
        self._archive_record = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def modified_at(self) -> datetime.datetime:
        """ DateTime the app config item was last modified """
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: datetime.datetime) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

    @property
    def path(self) -> List[str]:
        """ Array-based representation of config item's location in the tree in order from top to bottom. """
        if isinstance(self._path, Unset):
            raise NotPresentError(self, "path")
        return self._path

    @path.setter
    def path(self, value: List[str]) -> None:
        self._path = value

    @path.deleter
    def path(self) -> None:
        self._path = UNSET
