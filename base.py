#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:37:08 2019

@author: avmo
"""
from warnings import warn

from pyzotero import zotero, zotero_errors
from github import Github, UnknownObjectException

from _creds import KEY, USERID, GITHUB_ACCESS_TOKEN


class MyZotero(zotero.Zotero):
    def __init__(self):
        return super().__init__(USERID, "user", KEY)

    def get_collection(self, collection_name: str):
        return next(
            filter(
                lambda x: x["data"]["name"] == collection_name,
                self.all_collections(),
            )
        )

    def fix(self, items, apply_filters, apply_transforms, delete_fields, dry_run=True):
        """Magic method which iteratively applies filters (in-place changes),
        and transformations (changes based on other fields)

        Parameters
        ----------
        items : dict, {str: str}

        apply_filters : dict, {str: callable}

        apply_transforms: dict, {str: callable}

        delete_fields: iterable

        dry_run : bool

        Returns
        -------
        None
        """
        for item in items:
            # If the number of keys is zero, it was a deleted entry, or
            # otherwise uninteresting.
            if len(item["meta"].keys()):
                data = item["data"]
                for field, filters in apply_filters.items():
                    if field in data:
                        for fltr in filters:
                            item["data"][field], has_changed = fltr(data[field])
                            if has_changed:
                                print(field, "changed in", data["extra"])
                    else:
                        warn(f"No such field {field} in {list(data.keys())}")
                for fields, transform in apply_transforms.items():
                    field_in, *fields_out = fields
                    if field_in in data and "fixed" not in item["meta"]:
                        *new_field_values, has_changed = transform(data[field_in])
                        if has_changed:
                            item["data"].update(
                                {
                                    field: value
                                    for field, value in zip(
                                        fields_out, new_field_values
                                    )
                                }
                            )

                            print(
                                fields_out,
                                "transformed to",
                                new_field_values,
                                "in",
                                data["extra"],
                            )
                            item["meta"]["fixed"] = True
                    else:
                        warn(f"No such field {field_in} in {list(data.keys())}")

                for field in delete_fields:
                    if field in data:
                        del data[field]
                        del item["data"][field]

                if not dry_run:
                    try:
                        self.update_item(item)
                    except zotero_errors.UnsupportedParams as e:
                        print(item, e)
        if dry_run:
            print("WARNING: just a dry run")


class MyGithub(Github):

    def __init__(self):
        return super().__init__(GITHUB_ACCESS_TOKEN)

    def fetch_metadata(self, url):
        try:
            assert "github.com" in url

            repo = self.get_repo("/".join(url.split("/")[-2:]))

            item_type = "computerProgram"
            title = repo.description
            lang = repo.language
            try:
                rights = repo.get_license().license.name
            except UnknownObjectException:
                rights = None

            try:
                first, last = repo.owner.name.split()
            except ValueError:
                first = ""
                last = repo.owner.name
            creators = [
                {
                    "creatorType": "programmer",
                    "firstName": first,
                    "lastName": last,
                }
            ]
            catalog = "GitHub"
        except Exception as e:
            print(e)
            return [], False
        else:
            return item_type, title, creators, lang, rights, catalog, True


def strip_braces(field):
    updated_field = field.lstrip("{").rstrip("}")
    has_changed = updated_field != field
    if has_changed:
        print("Stripped braces from", field, "->", updated_field)
    return updated_field, has_changed


def lstrip_doi(field):
    updated_field = field.lstrip("http://dx.doi.org/")
    has_changed = updated_field != field
    if has_changed:
        print("Stripped http://dx.doi.org/ from", field, "->", updated_field)
    return updated_field, has_changed


def echo(field):
    print(field)
    return field, False


def fetch_github_metadata(url):
    g = MyGithub()
    return g.fetch_metadata(url)
