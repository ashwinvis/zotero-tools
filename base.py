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

    def fix(self, items, apply_filters, dry_run=True):
        for item in items:
            # If the number of keys is zero, it was a deleted entry, or
            # otherwise uninteresting.
            if len(item['meta'].keys()):
                data = item['data']
                for field, filters in apply_filters.items():
                    if field in data:
                        for fltr in filters:
                            item['data'][field], has_changed = fltr(data[field])
                            if has_changed:
                                print(field, "changed in", data["extra"])
                            else:
                                print(field, "unchanged in", data["extra"])
                if not dry_run:
                    self.update_item(item)
        if dry_run:
            print("WARNING: just a dry run")



def strip_braces(field):
    updated_field = field.lstrip('{').rstrip('}')
    has_changed = updated_field != field
    if has_changed:
        print("Stripped braces from", field, "->", updated_field)
    return updated_field, has_changed


def lstrip_doi(field):
    updated_field = field.lstrip('http://dx.doi.org/')
    has_changed = updated_field != field
    if has_changed:
        print("Stripped http://dx.doi.org/ from", field, "->", updated_field)
    return updated_field, has_changed


