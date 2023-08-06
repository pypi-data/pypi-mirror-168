# -*- coding: utf-8 -*-
# @Filename : object
# @Date : 2022-07-26-13-09
# @Project: nt-integration-sdk


from abc import ABC
from enum import Enum


def obj2dict(obj):
    if not hasattr(obj, "__dict__"):
        return obj
    result = {}
    for key, val in obj.__dict__.items():
        # avoiding exposure to the protect&private attribute
        if key.startswith("_"):
            continue
        element = []
        if isinstance(val, list):
            for item in val:
                element.append(obj2dict(item))
        else:
            element = obj2dict(val)
        result[key] = element
    return result


class NotionObject(ABC):
    @staticmethod
    def loads(**data):
        """Deserialize to python object

        Returns:

        """
        pass

    def export2json(self):
        """Export Object as Json Format

        Returns:

        """
        return obj2dict(self)

    def _auto_update_attributes(self, **kwargs):
        """Create all attributes that exist on variable `xargs` on current object

        Args:
            **xargs: args object

        """
        for key in kwargs.keys():
            self._update_attribute(key, kwargs[key])

    def _update_attribute(self, name, value):
        """Create an attribute on current object

        Args:
            name (string): attribute name
            value (any): attribute value

        """
        if value is not None:
            if isinstance(value, Enum):
                value = value.value
            setattr(self, name, value)

    def __getattr__(self, item):
        """
        Is an object method that is called if the object’s properties are not found.
        """
        return None
