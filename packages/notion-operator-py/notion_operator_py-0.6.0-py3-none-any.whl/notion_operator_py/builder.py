import os.path

from .objects import (
    NotionObject,
    Parent,
    Icon,
    Cover,
    Emoji,
    Properties
)


class BuilderObject(NotionObject):
    def edit_id(self, id: str):
        self._auto_update_attributes(id=id)

    def edit_parent(self, parent_id, parent_type='database_id'):
        self._auto_update_attributes(parent=Parent(parent_id=parent_id, parent_type=parent_type))

    def edit_archived(self, archived: bool):
        self._auto_update_attributes(archived=archived)

    def edit_last_edited_time(self, time: str):
        self._auto_update_attributes(last_edited_time=time)

    def edit_last_edited_by(self, user: dict):
        self._auto_update_attributes(last_edited_by=user)

    def edit_created_time(self, time: str):
        self._auto_update_attributes(created_time=time)

    def edit_created_by(self, user: dict):
        self._auto_update_attributes(created_by=user)


class PageAndDatabaseBuilder(BuilderObject):
    def edit_properties(self, title_key: str, title: str) -> Properties:
        self._auto_update_attributes(properties=Properties(key=title_key, title=title))
        return getattr(self, "properties")

    def edit_icon(self, icon: str, emoji: bool = False):
        self._auto_update_attributes(icon=Emoji(icon) if emoji else Icon(url=icon))

    def edit_cover(self, cover: str):
        self._auto_update_attributes(cover=(Cover(url=cover)))

    def edit_url(self, url: str):
        self._auto_update_attributes(url=url)
