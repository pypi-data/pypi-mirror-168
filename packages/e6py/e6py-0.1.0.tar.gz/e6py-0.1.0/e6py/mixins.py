from typing import Any, Dict, List, TYPE_CHECKING

import attr

from e6py.utils.serializer import to_dict

if TYPE_CHECKING:
    from e6py.client import E621Client


@attr.s()
class DictSerializationMixin:
    # Credit to dis-snek for this class
    @classmethod
    def _get_keys(cls) -> frozenset:
        if (keys := getattr(cls, "_keys", None)) is None:
            keys = frozenset(field.name for field in attr.fields(cls))
            setattr(cls, "_keys", keys)
        return keys

    @classmethod
    def _get_init_keys(cls) -> frozenset:
        if (init_keys := getattr(cls, "_init_keys", None)) is None:
            init_keys = frozenset(field.name.removeprefix("_") for field in attr.fields(cls) if field.init)
            setattr(cls, "_init_keys", init_keys)
        return init_keys

    @classmethod
    def _filter_kwargs(cls, kwargs_dict: dict, keys: frozenset) -> dict:
        return {k: v for k, v in kwargs_dict.items() if k in keys}

    @classmethod
    def _process_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process dictionary data received from e621. Does cleanup and other checks to data.

        Args:
            data: The dictionary data received from e621.

        Returns:
            The processed dictionary. Ready to be converted into object class.
        """
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any], client: "E621Client" = None):
        """
        Process and converts dictionary data received from e621 to object class instance.

        Args:
            data: The json data received from e621.
        """
        data = cls._process_dict(data)
        if client:
            data["client"] = client
        return cls(**cls._filter_kwargs(data, cls._get_init_keys()))

    @classmethod
    def from_list(cls, datas: List[Dict[str, Any]], client: "E621Client" = None):
        """
        Process and converts list data received from e621 to object class instances.

        Args:
            data: The json data received from e621.
        """
        return [cls.from_dict(data, client) for data in datas]

    def to_dict(self) -> Dict[str, Any]:
        """
        Exports object into dictionary representation, ready to be sent to e621.

        Returns:
            The exported dictionary.
        """
        return to_dict(self)
