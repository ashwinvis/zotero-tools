#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from base import MyZotero, echo, fetch_github_metadata, lstrip_doi, strip_braces

zot = MyZotero()

collection = zot.get_collection(
    "github-stars-ashwinvis"
)
# Get everything
items = zot.everything(zot.collection_items(collection["key"]))
apply_filters = {
    #  "Creators": (echo,)
    #  "DOI": (strip_braces, lstrip_doi),
    #  "pages": (lstrip_doi,)
}
apply_transforms = {
    (
        "url",
        "itemType",
        "title",
        "shortTitle",
        "abstractNote",
        "date",
        "creators",
        "programmingLanguage",
        "rights",
        "libraryCatalog",
    ): fetch_github_metadata
}
delete_fields = ("websiteTitle",)
to_process_item = lambda item: "fixed" not in item["meta"]
#  to_process_item = (
#      lambda item: "creators" not in item["data"] or not item["data"]["creators"]
#  )
zot.fix(
    items, apply_filters, apply_transforms, delete_fields, to_process_item,
    dry_run=False
)
