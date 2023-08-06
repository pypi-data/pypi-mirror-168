# -*- coding: utf-8 -*-
# @Filename : database_properties
# @Date : 2022-07-25-14-50
# @Project: nt-integration-sdk
import os
from abc import abstractmethod
from .common import Title, RichText, Select, Date, People, File, Formula, NotionObject, RelationC


class PropertyObject(NotionObject):
    @property
    @abstractmethod
    def _property_key(self) -> str:
        pass

    @property
    def property(self):
        return getattr(self, self._property_key, None)

    def _auto_update_attributes(self, value):
        self._update_attribute(self._property_key, value)


class TitleProperty(PropertyObject):
    @property
    def _property_key(self) -> str:
        return "title"

    def __init__(self, content: str):
        self._auto_update_attributes([Title(content)])


class RichTextProperty(PropertyObject):
    @property
    def _property_key(self) -> str:
        return "rich_text"

    def __init__(self, content: str, annotations: dict = None):
        self._auto_update_attributes([RichText(content, annotations)])


class NumberProperty(PropertyObject):
    @property
    def _property_key(self) -> str:
        return "number"

    def __init__(self, number: int):
        self._auto_update_attributes(number)


class SelectProperty(PropertyObject):
    @property
    def _property_key(self) -> str:
        return "select"

    def __init__(self, name: str, color: str = None):
        self._auto_update_attributes(Select(name=name, color=color))


class DateProperty(PropertyObject):
    @property
    def _property_key(self):
        return "date"

    def __init__(self, start: str, end: str = None, time_zone: str = None):
        self._auto_update_attributes(Date(start, end, time_zone))


class CheckBoxProperty(PropertyObject):
    @property
    def _property_key(self):
        return "checkbox"

    def __init__(self, checked: bool = False):
        self._auto_update_attributes(checked)


class URLProperty(PropertyObject):
    @property
    def _property_key(self):
        return "url"

    def __init__(self, url: str):
        self._auto_update_attributes(url)


class EmailProperty(PropertyObject):
    @property
    def _property_key(self):
        return "email"

    def __init__(self, email: str):
        self._auto_update_attributes(email)


class PhoneNumberProperty(PropertyObject):
    @property
    def _property_key(self):
        return "phone_number"

    def __init__(self, phone_number: str):
        self._auto_update_attributes(phone_number)


class FormulaProperty(PropertyObject):
    @property
    def _property_key(self):
        return "formula"

    def __init__(self, experssion: str):
        self._auto_update_attributes(Formula(experssion))


# todo: notion have not implemented those two API
# class RelationProperty(NotionObject):
# class RolloutProperty(NotionObject):


# --------------------------------------------------------
class MultiOptionsPropertyObject(PropertyObject):
    @property
    @abstractmethod
    def _property_key(self) -> str:
        pass

    def _add_property(self, value):
        getattr(self, self._property_key).append(value)

    def pop_property(self, index):
        getattr(self, self._property_key).pop(index)

    def remove_property(self, value):
        getattr(self, self._property_key).remove(value)


class MultipleSelectProperty(MultiOptionsPropertyObject):
    @property
    def _property_key(self):
        return "multi_select"

    def __init__(self, name: str, color: str = None):
        self._auto_update_attributes([Select(name=name, color=color)])

    def add_select(self, name: str, color: str = None):
        self._add_property(Select(name=name, color=color))


class PeopleProperty(MultiOptionsPropertyObject):
    @property
    def _property_key(self):
        return "people"

    def __init__(self, user_id: str):
        self._auto_update_attributes([People(user_id=user_id)])

    def add_people(self, user_id):
        self._add_property(People(user_id=user_id))


class FileProperty(MultiOptionsPropertyObject):
    @property
    def _property_key(self):
        return "files"

    def __init__(self, url: str):
        self._auto_update_attributes([File(name=os.path.basename(url), url=url)])

    def add_file(self, url: str):
        self._add_property(File(name=os.path.basename(url), url=url))


class RelationProperty(MultiOptionsPropertyObject):
    @property
    def _property_key(self) -> str:
        return "relation"

    def __init__(self, page_id: str):
        self._auto_update_attributes([RelationC(page_id)])

    def add_relation(self, page_id):
        self._add_property(RelationC(page_id))


# -------------------------------------------------
class Properties(NotionObject):
    def __init__(self, key: str, title: str):
        self._update_attribute(key, TitleProperty(title))

    def update_property(self, key, value: PropertyObject) -> PropertyObject:
        """Update Property

        Args:
            key (str): property key name
            value (str): property value

        Returns:
            Property Instance

        """
        if isinstance(value, PropertyObject) is False:
            raise TypeError(f"Property Object Type Error, {type(value)}")
        self._update_attribute(key, value)
        return self.get_property(key)

    def update_properties(self, properties: list) -> list:
        """Update Multiple Properies at one time

        Args:
            properties (list): list of tuple, include: property key and value

        Returns:
            List of property instances
        """
        properties_instances = []
        for key, value in properties:
            self.update_property(key, value)
            properties_instances.append(self.get_property(key))
        return properties_instances

    def get_property(self, key):
        """Get Property's value

        Args:
            key (str): property key name

        Returns:
            Property value
        """
        return getattr(self, key)

    def delete_property(self, key):
        delattr(self, key)

    def add_rich_text(self, key: str, plain_text: str, annotations: dict = None):
        return self.update_property(key, RichTextProperty(plain_text, annotations=annotations))

    def add_number(self, key: str, number: int):
        return self.update_property(key, NumberProperty(number))

    def add_select(self, key: str, select_name: str, select_color: str = None):
        return self.update_property(key, SelectProperty(select_name, select_color))

    def add_date(self, key: str, start: str, end: str = None, time_zone: str = None):
        return self.update_property(key, DateProperty(start, end, time_zone))

    def add_checkbox(self, key: str, checked: bool = False):
        return self.update_property(key, CheckBoxProperty(checked))

    def add_url(self, key: str, url: str):
        return self.update_property(key, URLProperty(url))

    def add_email(self, key: str, email: str):
        return self.update_property(key, EmailProperty(email))

    def add_phone_number(self, key: str, phone_number: str):
        return self.update_property(key, PhoneNumberProperty(phone_number))

    def add_formula(self, key: str, experssion: str):
        return self.update_property(key, FormulaProperty(experssion))

    def add_multiple_select(self, key: str, name: str, color: str = None):
        return self.update_property(key, MultipleSelectProperty(name=name, color=color))

    def add_people(self, key: str, user_id: str):
        return self.update_property(key, PeopleProperty(user_id=user_id))

    def add_file(self, key: str, url: str):
        return self.update_property(key, FileProperty(url=url))

    def add_relation(self, key: str, page_id: str):
        return self.update_property(key, RelationProperty(page_id))

