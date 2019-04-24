#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:37:08 2019

@author: avmo
"""
from pyzotero import zotero
from _creds import USERID, KEY


class MyZotero(zotero.Zotero):

    def __init__(self):
        return super().__init__(USERID, "user", KEY)

    def get_collection(self, collection_name: str):
        return next(
            filter(
                lambda x: x["data"]['name'] == collection_name,
                self.all_collections()
            )
        )
