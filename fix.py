#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from base import (
    MyZotero,
    echo,
    fetch_github_metadata,
    lstrip_doi,
    strip_braces,
)

zot = MyZotero()

thesis = zot.get_collection(
    #  "thesis"
    #  "paper_03_toy_model"
    # "paper_04_swe"
    "github-stars-ashwinvis"
)
# Get everything
items = zot.everything(zot.collection_items(thesis["key"]))
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
        "creators",
        "programmingLanguage",
        "rights",
        "libraryCatalog",
    ): fetch_github_metadata
}
delete_fields = ("websiteTitle",)
zot.fix(items, apply_filters, apply_transforms, delete_fields, dry_run=True)
