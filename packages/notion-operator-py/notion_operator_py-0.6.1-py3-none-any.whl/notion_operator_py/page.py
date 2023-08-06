# -*- coding: utf-8 -*-
# @Filename : database
# @Date : 2022-07-25-17-51
# @Project: nt-integration-sdk

import os
from notion_client.client import Client
from .builder import PageAndDatabaseBuilder


class PagePropertiesBuilder(PageAndDatabaseBuilder):
    pass


class Page:
    def __init__(self, client: Client = None):
        self.client = client if client else Client(auth=os.environ['NOTION_TOKEN'])

    def new_builder(self) -> PagePropertiesBuilder:
        return PagePropertiesBuilder()

    def get(self, page_id: str):
        return self.client.pages.retrieve(page_id)

    def update(self, page_id: str, builder: PagePropertiesBuilder):
        return self.client.pages.update(page_id=page_id, **builder.export2json())

    def create(self,
               builder: PagePropertiesBuilder,
               parent_id: str,
               parent_type: str = "database_id"):
        builder.edit_parent(parent_id=parent_id, parent_type=parent_type)
        return self.client.pages.create(**builder.export2json())
