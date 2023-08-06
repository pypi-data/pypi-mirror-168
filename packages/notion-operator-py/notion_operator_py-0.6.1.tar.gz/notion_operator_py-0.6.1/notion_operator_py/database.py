
import os
from notion_client.client import Client
from .builder import PageAndDatabaseBuilder
from .objects import RichText


class DatabasePropertiesBuilder(PageAndDatabaseBuilder):
    def edit_inline(self, inline: bool):
        self._auto_update_attributes(is_inline=inline)

    def edit_title(self, plain_text: str):
        self._auto_update_attributes(title=[RichText(content=plain_text)])

    def edit_description(self, description: str):
        self._auto_update_attributes(description=[RichText(content=description)])


class Database:
    def __init__(self, client: Client = None):
        self.client = client if client else Client(auth=os.environ['NOTION_TOKEN'])

    def new_builder(self) -> DatabasePropertiesBuilder:
        return DatabasePropertiesBuilder()

    def get(self, database_id: str):
        return self.client.databases.retrieve(database_id)

    def update(self, database_id: str, builder: DatabasePropertiesBuilder):
        return self.client.databases.update(database_id=database_id, **builder.export2json())

    def create(self,
               builder: DatabasePropertiesBuilder,
               parent_id: str,
               parent_type: str = "page_id"):
        builder.edit_parent(parent_id=parent_id, parent_type=parent_type)
        return self.client.databases.create(**builder.export2json())

    def query(self, database_id: str, filter: dict = None, sorts: dict = None):
        # "filter", "sorts", "start_cursor", "page_size"
        return self.client.databases.query(database_id=database_id, filter=filter, sorts=sorts)
