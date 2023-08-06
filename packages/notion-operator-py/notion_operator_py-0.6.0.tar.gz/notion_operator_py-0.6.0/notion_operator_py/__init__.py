# -*- coding: utf-8 -*-
# @Filename : __init__.py
# @Date : 2022-07-25-10-30
# @Project: nt-integration-sdk

from notion_client.client import Client
from .database import Database
from .page import Page


class IntegrationClient:
    def __init__(self, auth: str):
        self.client = Client(auth=auth)

    def page(self) -> Page:
        return Page(self.client)

    def database(self) -> Database:
        return Database(self.client)


__all__ = [
    "IntegrationClient"
]
